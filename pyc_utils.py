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


class RuleWBLA(FixedRules):
    """
    Rules with ability to incorporate BLAs
    """

    main: Site
    rules: RuleStore
    choice: Choice
    by: KeyForm
    updated_main: Site

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
        self.bla_main = Site(self.rules.main.index, {}, 0.0)
        self.choice.input = self.bla_main


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