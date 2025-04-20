from pyClarion import Input, Choice, Agent, Event, Priority, Family, Atoms, Atom, BaseLevel, Pool, NumDict, IDN, Train
from pyClarion.components.stats import MatchStats


from utils import *
from knowledge_init import *

from datetime import timedelta
import math


class BaseParticipant(Agent):  
    construction_space: BrickConstructionTask
    search_space_rules: RuleWBLA
    search_space_blas: BaseLevel
    search_space_matchstats: MatchStats
    search_space_pool: Pool
    search_space_choice: Choice
    
    construction_input: Input

    response_space: BrickResponseTask
    response_input: Input
    response_rules: RuleWBLA
    response_blas: BaseLevel
    response_pool: Pool
    response_choice: Choice

    #TODO: fill in the rest here once ur done below

    def __init__(self, name: str, **kwargs) -> None:
        p = Family()
        e = Family() 

        r_construction  = Family() # rule family for construction rules
        r_response = Family() # rule family for response rules
        c_construction = Family() # construction family for construction chunks
        c_response = Family() # response family for response chunks

        response_space = BrickResponseTask() 
        construction_space = kwargs.get("construction_space", BrickConstructionTask()) # default to the construction space
        if "construction_space" in kwargs: del kwargs["construction_space"]

        super().__init__(name, p=p, e=e, 
                         construction_space= construction_space,response_space=response_space, 
                         r_construction=r_construction, r_response=r_response, 
                         c_construction=c_construction, c_response=c_response, 
                         **kwargs)
        self.p = p
        self.e = e
        self.response_space = response_space
        self.construction_space = construction_space

        with self:
            self.construction_input = FlippableInput("construction_input", (construction_space, construction_space), reset=False)
            self.response_input = FlippableInput("response_input",  (response_space, response_space), reset=True)

            self.response_rules = RuleWBLA("response_rules", p=p, r=r_response, c=c_response, d=response_space, v=response_space, sd=1e-4)
            self.search_space_rules = RuleWBLA("search_space_rules", p=p, r=r_construction, c=c_construction, d=construction_space, v=construction_space, sd=1e-4)

            #TODO: this good?
            self.search_space_matchstats = MatchStats("search_space_matchstats", p, self.search_space_rules.rules.rules, th_cond=0.9, th_crit=0.9) # 0.9 because i want to compare against 1.
            
            self.response_pool = Pool("pool", p, self.response_rules.rules.rules, func=NumDict.sum) # to pool together the blas and condition activations
            self.search_space_pool = Pool("search_space_pool", p, self.search_space_rules.rules.rules, func=NumDict.sum) # similar function

            self.response_choice = Choice("choice", p, (response_space, response_space), sd=1e-2)
            self.search_space_choice = Choice("search_space_choice", p, (construction_space, construction_space), sd=1e-2)

        self.response_rules.rules.lhs.bu.input = self.response_input.main 
        self.search_space_rules.rules.lhs.bu.input = self.construction_input.main

        self.search_space_pool["search_spaces_rules.rules"] = (
            self.search_space_rules.rules.main,  
            lambda d: d.shift(x=1).scale(x=0.5).logit())
        self.response_pool["response_rules.rules"] = (
            self.response_rules.rules.main,
            lambda d: d.shift(x=1).scale(x=0.5).logit()) # you can take atmost 0.2 points of activation off using matchstats 
        #TODO: the contribution of matchstats should be weakened as the neural network gets better ?
        
        self.search_space_pool["search_space_matchstats"] = (
            self.search_space_matchstats.main, 
            lambda d: d.exp().shift(x=1).inv().scale(0.2)) # TODO: is the function here correct?
        
        self.response_rules.bla_main = self.response_pool.main #updated site for the response rules to take BLAS into account
        self.search_space_rules.bla_main = self.search_space_pool.main
        #rewire choice input
        self.search_space_rules.choice.input = self.search_space_pool.main
        self.response_rules.choice.input = self.response_pool.main

        self.response_choice.input = self.response_rules.rules.rhs.td.main # bu choice
        self.search_space_choice.input = self.search_space_rules.rules.rhs.td.main
        
        #backtracking queues: #TODO: use BLA queue
        self.past_constructions = []
        self.past_chosen_rules = []
        self.all_rule_history = []

        #wait events for low level pool update;
        self.search_space_trigger_wait = []
        self.response_trigger_wait = []

        self.trigger_response = False #TODO: prolly dont need this here. 

    def resolve(self, event: Event) -> None:
        # -- RESPONSE PROCESSING --
        # if event.source == self.response_rules.rules.update: # after the rules have updated 
        #     self.response_blas.update() # timestep update
        if event.source == self.response_pool.update and \
            self.trigger_response \
            and all(e.source not in self.response_trigger_wait for e in self.system.queue):
            self.response_rules.trigger()
        elif event.source == self.response_rules.rules.rhs.td.update:
            self.response_choice.trigger() #poll outside the loop in experimental loop
        elif event.source == self.start_response_trial:
            self.trigger_response = True
        
        # -- SEARCH PROCESSING --
        elif event.source == self.start_construct_trial:
            self.trigger_response = False
        elif event.source == self.construction_input.send:
            self.past_constructions.append(self.construction_input.main[0]) # add the current construction to the past constructions    
        
        elif event.source == self.search_space_rules.rules.update:
            self.search_space_matchstats.update() # update the match stats
        
        elif event.source == self.search_space_pool.update \
            and all(e.source not in self.search_space_trigger_wait for e in self.system.queue):
            self.search_space_rules.trigger()
        
        elif event.source == self.search_space_rules.rules.rhs.td.update:
            self.search_space_choice.trigger()
        
        elif event.source == self.search_space_choice.select:
            self.resolve_lowlevel_search_choice(event)
        
        elif event.source == self.search_space_matchstats.increment:
            # make the mask zero:
            new_empty_mask = self.search_space_matchstats.cond.new({}).with_default(c=0.0)
            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.cond.data.append(new_empty_mask)
            self.search_space_matchstats.discount()#TODO: apt timedelta?

        elif event.source == self.search_space_matchstats.discount and any(e.source == self.end_construction_feedback for e in self.system.queue):
                self.propagate_feedback()

        elif event.source == self.end_construction:
            # clear system queue
            self.system.queue.clear() # at this point, you should have a clear target_grid representation built -- correct or incorrect

    def start_construct_trial(self, 
        dt: timedelta, 
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.system.schedule(self.start_construct_trial, dt=dt, priority=priority)

    def resolve_lowlevel_search_choice(self, event: Event) -> None:
        raise NotImplementedError
    
    def end_construction(self, 
                         dt: timedelta = timedelta(seconds=0),
                         priority: Priority = Priority.PROPAGATION
                         ) -> None:
        self.system.schedule(self.end_construction, dt=dt, priority=priority)

    def end_construction_feedback(self,
                                  dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.system.schedule(self.end_construction_feedback, dt=dt, priority=priority)

    def start_response_trial(self, 
        dt: timedelta, 
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.response_input.send(make_response_input(self.construction_input.main[0], self.response_input.main[0].i).d) # send the construction input to the response input
        self.system.schedule(self.start_response_trial, dt=dt, priority=priority)
    
    def finish_response_trial(self,
                              dt: timedelta,
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.system.schedule(self.finish_response_trial, dt=dt, priority=priority)

    def propagate_feedback(self, correct:float = 0) -> None:
        if not self.past_chosen_rules:
            return
        
        rule = self.past_chosen_rules.pop()
        #is there a correct already in there?:
        if self.search_space_matchstats.crit[0].c:
            correct = 1.0

        new_rule_mask = self.search_space_matchstats.cond.new({rule: 1.0}).with_default(c=0.0)
        new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=correct)

        self.search_space_matchstats.cond.data.pop()
        self.search_space_matchstats.crit.data.pop()

        self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition to only change scores for this rule
        self.search_space_matchstats.crit.data.append(new_crit_score)
        
        self.search_space_matchstats.increment() # TODO: apt timedelta?

class LowLevelParticipant(BaseParticipant):  

    def __init__(self, name: str) -> None:
        super().__init__(name=name)

        self.search_space_trigger_wait = [self.search_space_pool.update]
        self.response_trigger_wait = [self.response_rules.rules.update]

    def resolve_lowlevel_search_choice(self, event):
        #check if indeed we need to stop construction, if triggered the STOP rule
        cur_rule_sample = self.search_space_rules.choice.sample
        cur_rule_choice = self.search_space_rules.choice.poll()
        cur_rule_number = list(cur_rule_choice.values())[0][-1:][0][0]

        cur_choice = self.search_space_choice.poll()

        if cur_choice[~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens] == ~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens.backtrack_construction: #backtrack
            new_rule_mask = self.search_space_matchstats.cond.new({list(cur_rule_choice.values())[0]: 1.0}).with_default(c=0.0)
            new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=0.0)#we want to increment the negativity count
            
            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.crit.data.pop()

            self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition ot only change scores for this rule
            self.search_space_matchstats.crit.data.append(new_crit_score) 

            self.search_space_matchstats.increment() # TODO: apt timedelta?
            last_construction = self.past_constructions.pop()
            self.past_chosen_rules.pop()
            self.construction_input.send(last_construction, flip=True) # pop the last construction, also make sure to reset: flip is false as initialized with reset = false

        elif cur_choice[~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens] == ~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens.stop_construction:
            self.end_construction() # TODO: consider adding stop construction rules to rule history for matchstats
        else: #continue construction
            self.past_chosen_rules.append(list(cur_rule_choice.values())[0])
            self.all_rule_history.append(list(cur_rule_choice.values())[0])
            self.construction_input.send(filter_keys_by_rule_chunk(self.search_space_rules.rules.rhs.chunks._members_[Key(f"{cur_rule_number}")], self.search_space_choice.main[0].d)) # loop it back in --for more selections

class AbstractParticipant(BaseParticipant):  
    """
    Contains everything the non-abstract participant does with the added features:
    1. RL and MLP is now over the ryles
    2. there is an abstract rule space -- with choices, and pools over the same
    3. A choice in the abstract space leads to a downstream impact on the construction space
    4. This downstream impact influences activations of low-level construction choices
    5. Which prgoresses by way of rule activations, blas, and math statistics
    """

    def __init__(self, name: str) -> None:
        r_abstract = Family() # rule family for abstract rules
        c_abstract = Family() # abstract family for abstract chunks

        construction_space = BrickConstructionTaskAbstractParticipant()
        abstract_space = HighLevelConstruction() 

        super().__init__(name,
                         construction_space=construction_space, abstract_space=abstract_space,
                         r_abstract=r_abstract,
                         c_abstract=c_abstract,)
        with self:
            self.abstract_construction_input = Input("abstract_construction_input", (abstract_space, abstract_space), reset=False)

            self.abstract_space_rules = RuleWBLA("abstract_space_rules", p=self.p, r=r_abstract, c=c_abstract, d=abstract_space, v=abstract_space, sd=1e-4)

            self.abstract_space_matchstats = MatchStats("abstract_space_matchstats", self.p, self.abstract_space_rules.rules.rules, th_cond=0.9, th_crit=0.9) # 0.9 because i want to compare against 1.
            self.abstract_space_pool = Pool("abstract_space_pool", self.p, self.abstract_space_rules.rules.rules, func=NumDict.sum) # similar function
            self.abstract_space_choice = Choice("abstract_space_choice", self.p, (abstract_space, abstract_space))

        self.abstract_space_rules.rules.lhs.bu.input = self.abstract_construction_input.main

        self.abstract_space_pool["abstract_space_rules.rules"] = (
            self.abstract_space_rules.rules.main,
            lambda d: d.shift(x=1).scale(x=0.5).logit())
        
        self.abstract_space_pool["abstract_space_matchstats"] = (
            self.abstract_space_matchstats.main,
            lambda d: d.exp().shift(x=1).inv().scale(0.2))
        
        self.abstract_space_rules.choice.input = self.abstract_space_pool.main

        
        self.abstract_space_choice.input = self.abstract_space_rules.rules.rhs.td.main
        
        #extra backtracking queues: #TODO: better way to do this is probably with Sites, adn their inbuilt deque
        self.past_chosen_rules_abstract = []
        self.all_rule_history_abstract = []

        self.search_space_trigger_wait = [self.search_space_pool.update, self.abstract_search_space_pool.update]
        self.abstract_space_trigger_wait = [self.abstract_space_pool.update]
        self.response_trigger_wait = [self.response_rules.rules.update]

    def resolve(self, event: Event) -> None:
        super().resolve(event)

        # ABSTRACT SEARCH PROCESSING
        if event.source == self.abstract_space_rules.rules.update:
            self.abstract_space_matchstats.update()
        
        elif event.source == self.abstract_space_pool.update and all(e.source not in self.abstract_space_trigger_wait for e in self.system.queue):
            self.abstract_space_rules.trigger()
        
        elif event.source == self.abstract_space_rules.rules.rhs.td.update:
            self.abstract_space_choice.trigger()
        
        elif event.source == self.abstract_space_choice.select:
            cur_sample = self.abstract_space_rules.choice.sample
            cur_rule_choice = self.abstract_space_rules.choice.poll()
            cur_rule_number = list(cur_rule_choice.values())[0][-1:][0][0]
            cur_choice = self.abstract_space_choice.poll()

            if cur_choice[~self.abstract_space.io.stop * ~self.abstract_space.response] == ~self.abstract_space.io.stop * ~self.abstract_space.response.yes:
                self.end_construction()
            else:
                self.past_chosen_rules_abstract.append(list(cur_rule_choice.values())[0])
                self.all_rule_history_abstract.append(list(cur_rule_choice.values())[0])
                self.construction_input.send(filter_keys_by_rule_chunk(self.abstract_space_rules.rules.rhs.chunks._members_[Key(f"{cur_rule_number}")], self.abstract_space_choice.main[0].d)) # #TODO: does this add or replace?
        
        elif self.abstract_space_matchstats.increment:
            # make the mask zero:
            new_empty_mask = self.abstract_space_matchstats.cond.new({}).with_default(c=0.0)
            self.abstract_space_matchstats.cond.data.pop()
            self.abstract_space_matchstats.cond.data.append(new_empty_mask)
            self.abstract_space_matchstats.discount()
        
        elif event.source == self.abstract_space_matchstats.discount and any(e.source == self.end_construction_feedback for e in self.system.queue):
                self.propagate_abstract_feedback()

    def propagate_abstract_feedback(self, 
                           correct:float = 0) -> None:
        
        if not self.past_chosen_rules_abstract:
            return
        if self.abstract_search_space_matchstats.crit[0].c:
            correct = 1.0
        
        rule = self.past_chosen_rules_abstract.pop()
        
        new_rule_mask = self.abstract_space_matchstats.cond.new({rule: 1.0}).with_default(c=0.0)
        new_crit_score = self.abstract_space_matchstats.crit.new({}).with_default(c=correct)

        self.abstract_space_matchstats.cond.data.pop()
        self.abstract_space_matchstats.crit.data.pop()

        self.abstract_space_matchstats.cond.data.append(new_rule_mask) # update the condition to only change scores for this rule
        self.abstract_space_matchstats.crit.data.append(new_crit_score)
        
        self.abstract_space_matchstats.increment() # TODO: apt timedelta?
