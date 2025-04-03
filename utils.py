from pyClarion import FixedRules, Choice
from pyClarion import Site, RuleStore, Choice, KeyForm, Family, Sort, Atom

from typing import *

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
        self.choice.input = self.bla_main