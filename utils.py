from pyClarion import FixedRules, Choice
from pyClarion import Site, RuleStore, Choice, KeyForm, Family, Sort, Atom, V, DV, Event, Priority

from typing import *
from time import timedelta

class RuleWBLA(FixedRules):
    main: Site
    rules: RuleStore
    choice: Choice
    by: KeyForm
    updated_main: Site

    def __init__(self, 
        name: str, 
        p: Family,
        r: Family,
        c: Family, 
        d: Family | Sort | Atom, 
        v: Family | Sort,
        *,
        sd: float = 1.0
    ) -> None:
        
        super().__init__(name, p=p, r=r, c=c, d=d, v=v, sd=sd)
        self.bla_main = Site(self.rules.main.index, {}, 0.0)
        self.choice.input = self.bla_main.main

class LaggedChoice(Choice):
    def __init__(self, 
        name: str, 
        p: Family, 
        s: V | DV, 
        *, 
        sd: float = 1.0
    ) -> None:
        super().__init__(name, p=p, s=s, sd=sd)
    
    @override
    def resolve(self, event: Event) -> None:
        if event.source == self.trigger:
            self.select()
            self.select_complete()

    def select_complete(self, 
                        dt: timedelta = timedelta(),
                        priority=Priority.CHOICE) -> None:
        self.system.schedule(
            self.select_complete,
            dt=dt,
            priority=priority
        )
