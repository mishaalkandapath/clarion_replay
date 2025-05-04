from typing import override
from datetime import timedelta

from utils import write_inplace_consistent
from pyClarion import (
    FixedRules,
    RuleStore,
    Choice,
    KeyForm,
    Site,
    Family,
    Sort,
    Atom,
    Chunk,
    ChunkStore,
    BottomUp,
    Input,
    Priority,
    keyform,
)


class FlippableInput(Input):
    """
    Input process that can be flipped to either reset or write in place
    """
    @override
    def send(
        self,
        d: dict | Chunk,
        dt: timedelta = timedelta(),
        priority: int = Priority.PROPAGATION,
        flip: bool = False,
    ):
        reset = self.reset if not flip else not self.reset
        data = self._parse_input(d)
        method = Site.push if reset else write_inplace_consistent
        self.system.schedule(
            self.send, self.main.update(data, method), dt=dt, priority=priority
        )


"""
Revised processes to account for suppressed
-ve weighted chunks within dimension.
"""


class SuppressionBottomUp(BottomUp):
    @override
    def update(
        self, dt: timedelta = timedelta(), priority: int = Priority.PROPAGATION
    ) -> None:
        ipt = self.input[0]
        if self.pre is not None:
            ipt = self.pre(ipt)
        main = self.weights[0].mul(ipt, by=self.mul_by)
        temp = main.max(by=self.max_by)
        another_temp = main.min(by=self.max_by).simple_where(lambda x: x < 0.0)
        main = temp.sum(another_temp).sum(by=self.sum_by)
        main = main.simple_where(lambda x: x >= 0.0).with_default(c=0.0)
        if self.post is not None:
            main = self.post(main)
        self.system.schedule(
            self.update, self.main.update(main), dt=dt, priority=priority
        )


class SupressionChunkStore(ChunkStore):
    def __init__(
        self, name: str, c: Family, d: Family | Sort | Atom, v: Family | Sort
    ) -> None:
        super().__init__(name, c=c, d=d, v=v)
        with self:
            self.bu = SuppressionBottomUp(f"{name}.bu", self.chunks, c, d, v)


class SuppressionRuleStore(RuleStore):
    def __init__(
        self,
        name: str,
        r: Family,
        c: Family,
        d: Family | Sort | Atom,
        v: Family | Sort,
    ) -> None:
        super().__init__(name, r=r, c=c, d=d, v=v)
        with self:
            self.lhs = SupressionChunkStore(f"{name}.lhs", c, d, v)
        idx_r = self.system.get_index(keyform(self.rules))
        idx_lhs = self.system.get_index(keyform(self.lhs.chunks))
        idx_rhs = self.system.get_index(keyform(self.rhs.chunks))
        self.main = Site(idx_r, {}, c=0.0)
        self.riw = Site(idx_r * idx_r, {}, c=float("nan"))
        self.lhw = Site(idx_r * idx_lhs, {}, c=float("nan"))
        self.rhw = Site(idx_r * idx_rhs, {}, c=float("nan"))


class SupressionActionRules(FixedRules):
    bla_main: Site 
    def __init__(
        self,
        name: str,
        p: Family,
        r: Family,
        c: Family,
        d: Family | Sort | Atom,
        v: Family | Sort,
        *,
        sd: float = 1.0,
    ) -> None:
        super().__init__(name, p=p, r=r, c=c, d=d, v=v, sd=sd)
        with self:
            self.rules = SuppressionRuleStore(f"{name}.rules", r, c, d, v)
            self.choice = Choice(f"{name}.choice", p, self.rules.rules, sd=sd)
        self.main = Site(self.rules.main.index, {}, 0.0)
        self.mul_by = keyform(self.rules.rules).agg * keyform(self.rules.rules)
        self.sum_by = keyform(self.rules.rules) * keyform(self.rules.rules).agg
        self.choice.input = self.rules.main
        self.bla_main = Site(self.rules.main.index, {}, 0.0)
        self.choice.input = self.bla_main
        