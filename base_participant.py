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
            self.construction_input = Input("construction_input", (construction_space, construction_space))
            self.response_input = Input("response_input",  (response_space, response_space), reset=False)

            self.response_rules = RuleWBLA("response_rules", p=p, r=r_response, c=c_response, d=response_space, v=response_space, sd=1e-4)
            self.search_space_rules = RuleWBLA("search_space_rules", p=p, r=r_construction, c=c_construction, d=construction_space, v=construction_space, sd=1e-4)
            
            self.response_blas = BaseLevel("blas", p, e, self.response_rules.rules.rules)
            self.search_space_blas = BaseLevel("search_space_blas", p, e, self.search_space_rules.rules.rules)
            self.response_blas.ignore.add(~self.response_rules.rules.rules.nil) 
            self.search_space_blas.ignore.add(~self.search_space_rules.rules.rules.nil)

            #TODO: this good?
            self.search_space_matchstats = MatchStats("search_space_matchstats", p, self.search_space_rules.rules.rules, th_cond=0.9, th_crit=0.9) # 0.9 because i want to compare against 1.
            
            self.response_pool = Pool("pool", p, self.response_rules.rules.rules, func=NumDict.sum) # to pool together the blas and condition activations
            self.search_space_pool = Pool("search_space_pool", p, self.search_space_rules.rules.rules, func=NumDict.sum) # similar function

            self.response_choice = Choice("choice", p, (response_space, response_space))
            self.search_space_choice = Choice("search_space_choice", p, (construction_space, construction_space))
        
        self.response_blas.input = self.response_rules.choice.main
        self.search_space_blas.input = self.search_space_rules.choice.main

        self.response_rules.rules.lhs.bu.input = self.response_input.main 
        self.search_space_rules.rules.lhs.bu.input = self.construction_input.main

        self.search_space_pool["search_spaces_rules.rules"] = (
            self.search_space_rules.rules.main,  
            lambda d: d.shift(x=1).scale(x=0.5).logit())
        self.response_pool["response_rules.rules"] = (
            self.response_rules.rules.main,
            lambda d: d.shift(x=1).scale(x=0.5).logit())
        
        self.response_pool["blas"] = (
            self.response_blas.main, 
            lambda d: d.bound_min(x=1e-8).log().with_default(c=0.0))
        self.search_space_pool["blas"] = (
            self.search_space_blas.main,
            lambda d: d.bound_min(x=1e-8).log().with_default(c=0.0))
        
        self.search_space_pool["search_space_matchstats"] = (
            self.search_space_matchstats.main, 
            lambda d: d.bound_min(x=1e-8).log().with_default(c=0.0)) # TODO: is the function here correct?
        
        self.response_rules.bla_main = self.response_pool.main #updated site for the response rules to take BLAS into account
        self.search_space_rules.bla_main = self.search_space_pool.main
        #rewire choice input
        self.search_space_rules.choice.input = self.search_space_pool.main
        self.response_rules.choice.input = self.response_pool.main

        self.response_choice.input = self.response_rules.rules.rhs.td.main # bu choice
        self.search_space_choice.input = self.search_space_rules.rules.rhs.td.main

        with self.response_pool.params[0].mutable():
            self.response_pool.params[0][~self.response_pool.p["blas"]] = 2e-1
        with self.search_space_pool.params[0].mutable():
            self.search_space_pool.params[0][~self.search_space_pool.p["blas"]] = 2e-1
        
        #backtracking queues: #TODO: better way to do this is probably with Sites, adn their inbuilt deque
        self.past_constructions = []
        self.past_chosen_rules = []
        self.all_rule_history = []

        #wait events for low level pool update;
        self.search_space_trigger_wait = []

    def resolve(self, event: Event) -> None:
        # -- RESPONSE PROCESSING --
        if event.source == self.response_rules.rules.update: # after the rules have updated 
            self.response_blas.update() # timestep update
        elif event.source == self.response_pool.update: # TODO: is this right?
            self.response_rules.trigger()
        elif event.source == self.response_rules.rules.rhs.td.update:
            self.response_choice.trigger() #poll outside the loop in experimental loop
        
        # -- SEARCH PROCESSING --
        elif event.source == self.search_space_rules.rules.update:
            if not self.past_constructions: self.past_constructions = [self.construction_input.main[0]]
            self.search_space_blas.update()
            self.search_space_matchstats.update() # update the match stats
        
        elif event.source == self.search_space_pool.update and all(e.source not in self.search_space_trigger_wait for e in self.system.queue):
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

        elif event.source == self.end_construction:
            # clear system queue
            self.system.queue.clear() # at this point, you should have a clear target_grid representation built -- correct or incorrect
        
        elif event.source == self.propagate_feedback:
            self.end_construction_feedback()

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
        self.system.schedule(self.start_response_trial, dt=dt, priority=priority)
    
    def finish_response_trial(self,
                              dt: timedelta,
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.system.schedule(self.finish_response_trial, dt=dt, priority=priority)

    def propagate_feedback(self, 
                           dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION,
                           correct:float = 0) -> None:
        
        for rule in self.past_chosen_rules:
            new_rule_mask = self.search_space_matchstats.cond.new({rule: 1.0}).with_default(c=0.0)
            new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=correct)

            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.crit.data.pop()

            self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition to only change scores for this rule
            self.search_space_matchstats.crit.data.append(new_crit_score)
            
            self.search_space_matchstats.increment() # TODO: apt timedelta?
            self.search_space_matchstats.discount()
            self.schedule(self.propagate_feedback, dt=dt, priority=priority)

class LowLevelParticipant(BaseParticipant):  

    def __init__(self, name: str) -> None:

        #RL components
        h = Family() # hidden layer information
        mlp_space_1 = MLPConstructionIO() # input space for the MLP
        mlp_space_2 = Numbers() # output space for the MLP

        super().__init__(name=name, h=h, mlp_space_1=mlp_space_1, mlp_space_2=mlp_space_2)

        self.mlp_space_1 = mlp_space_1
        self.mlp_space_2 = mlp_space_2

        with self:
            self.mlp_construction_input = Input("mlp_construction_input", (mlp_space_1, mlp_space_2), reset=False)

            # RL Construction
            with self.search_space_rules.choice:
                self.construction_net = self.mlp_construction_input >> IDN("construction_net", 
                                                                    p=self.p, 
                                                                    h=h,
                                                                    r=self.search_space_rules.rules.rules, # reward specification on rule choice
                                                                    s1=(mlp_space_1, mlp_space_2), #input construction space has goal state and current state
                                                                    s2=self.search_space_rules.rules.rules,
                                                                    layers=(),#(512, 256, 512),
                                                                    train=Train.WEIGHTS,
                                                                    gamma=.3,
                                                                    lr=1e-2
                                                                    )
        
        self.search_space_pool["search_space_netscores"] = (
            self.construction_net.olayer.main,
            lambda d: d.bound_min(x=1e-8).log().with_default(c=0.0)) # TODO: verify this scaling..

        #RL stats
        self.construction_reward_vals = []
        self.construction_qvals = []
        self.construction_net_training_results = []

        self.search_space_trigger_wait = [self.search_space_pool.update]

    def resolve(self, event: Event) -> None:

        super().resolve(event)
        if event.source == self.construction_net.error.update:
            self.construction_net_training_results.append(self.construction_net.error.main[0].pow(x=2.0))

    def resolve_lowlevel_search_choice(self, event):
        #check if indeed we need to stop construction, if triggered the STOP rule
        cur_sample = self.search_space_rules.choice.sample
        cur_rule_choice = self.search_space_rules.choice.poll()
        
        temp_sample = cur_sample.new(cur_sample[0]._d).with_default(c=-math.inf)
        temp_sample = temp_sample.exp().div(temp_sample.exp().sum())
        cur_sample.data.pop()
        cur_sample.data.append(temp_sample) # simple copy for softmaxing activation

        cur_choice = self.search_space_choice.poll()

        if cur_sample[0][list(cur_rule_choice.values())[0]] < 0.2: #backtrack # TODO: guaranteed to be list of size 1 yea?
            new_rule_mask = self.search_space_matchstats.cond.new({list(cur_rule_choice.values())[0]: 1.0}).with_default(c=0.0)
            new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=0.0)#we want to increment the negativity count
            
            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.crit.data.pop()

            self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition ot only change scores for this rule
            self.search_space_matchstats.crit.data.append(new_crit_score) 

            self.search_space_matchstats.increment() # TODO: apt timedelta?
            last_construction = self.past_constructions.pop()
            self.construction_input.send(last_construction) # pop the last construction
            self.mlp_construction_input.send(mlpify(last_construction, self.mlp_construction_input.main.index))

            # also give -1 reward to the rule that was chosen 
            self.construction_net.error.send({list(cur_rule_choice.values())[0]: -1.0}) # TODO: check this
            self.construction_reward_vals.append(-1.0)
            self.construction_qvals.append(self.search_space_pool["search_space_netscores"][0].max().c)

        elif cur_choice[~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens] == ~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens.stop_construction: # TODO: check this
            self.end_construction()
            self.response_input.send(self.search_space_choice.main[0]) # send the choice to the response input -- to make a decision out of 
        else: #continue construction
            self.past_constructions.append(self.search_space_choice.main[0])
            self.past_chosen_rules.append(cur_sample[0][list(cur_rule_choice.values())[0]])
            self.all_rule_history.append(cur_sample[0][list(cur_rule_choice.values())[0]])
            self.construction_input.send(self.search_space_choice.main[0]) # loop it back in --for more selections
            self.mlp_construction_input.send(mlpify(self.search_space_choice.main[0], self.mlp_construction_input.main.index)) # TODO: check this
    
    @override
    def start_construct_trial(self, 
        dt: timedelta, 
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        # the previous construction trial has ended, so clear TD trackers
        self.construction_net.error.reward.data.clear() # TODO: anyway to schedule such changes than doing it here?
        self.construction_net.error.qvals.data.clear()
        self.construction_net.error.action.data.clear()

        #add new 0-default entries
        self.construction_net.error.reward.data.append(self.construction_net.error.reward.new({}).with_default(c=0.0))
        self.construction_net.error.qvals.data.append(self.construction_net.error.qvals.new({}).with_default(c=0.0))
        self.construction_net.error.action.data.append(self.construction_net.error.action.new({}).with_default(c=0.0))
        

        self.system.schedule(self.start_construct_trial, dt=dt, priority=priority)

    @override
    def propagate_feedback(self, 
                           dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION,
                           correct:float = 0) -> None:
        
        for rule in self.past_chosen_rules:
            new_rule_mask = self.search_space_matchstats.cond.new({rule: 1.0}).with_default(c=0.0)
            new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=correct)

            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.crit.data.pop()

            self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition to only change scores for this rule
            self.search_space_matchstats.crit.data.append(new_crit_score)
            
            self.search_space_matchstats.increment() # TODO: apt timedelta?
            self.search_space_matchstats.discount()
            self.schedule(self.propagate_feedback, dt=dt, priority=priority)

            #update similarly the construction net
            self.construction_net.error.send({rule: correct})
            self.construction_reward_vals.append(correct)
            self.construction_qvals.append(self.search_space_pool["search_space_netscores"][0].max().c)

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

        #RL components
        h = Family() # hidden layer information
        mlp_space_1 = MLPConstructionIO() # input space for the MLP
        mlp_space_2 = Numbers() # output space for the MLP

        super().__init__(name, h=h,
                         construction_space=construction_space, abstract_space=abstract_space,
                         r_abstract=r_abstract,
                         c_abstract=c_abstract,
                         mlp_space_1=mlp_space_1, mlp_space_2=mlp_space_2)
        self.mlp_space_1 = mlp_space_1
        self.mlp_space_2 = mlp_space_2

        with self:
            self.mlp_construction_input = Input("mlp_construction_input", (mlp_space_1, mlp_space_2), reset=False)
            self.abstract_construction_input = Input("abstract_construction_input", (abstract_space, abstract_space), reset=False)

            self.abstract_space_rules = RuleWBLA("abstract_space_rules", p=self.p, r=r_abstract, c=c_abstract, d=abstract_space, v=abstract_space, sd=1e-4)
            
            self.abstract_space_blas = BaseLevel("abstract_space_blas", self.p, self.e, self.abstract_space_rules.rules.rules)
            self.abstract_space_blas.ignore.add(~self.abstract_space_rules.rules.rules.nil)

            self.abstract_space_matchstats = MatchStats("abstract_space_matchstats", self.p, self.abstract_space_rules.rules.rules, th_cond=0.9, th_crit=0.9) # 0.9 because i want to compare against 1.
            self.abstract_space_pool = Pool("abstract_space_pool", self.p, self.abstract_space_rules.rules.rules, func=NumDict.sum) # similar function
            self.abstract_space_choice = Choice("abstract_space_choice", self.p, (abstract_space, abstract_space))

            # RL Construction
            with self.abstract_space_rules.choice:
                self.construction_net = self.mlp_construction_input >> IDN("construction_net", 
                                                                    p=self.p, 
                                                                    h=h,
                                                                    r=self.abstract_space_rules.rules.rules, # reward specification on rule choice
                                                                    s1=(mlp_space_1, mlp_space_2), #input construction space has goal state and current state
                                                                    s2=self.abstract_space_rules.rules.rules,
                                                                    layers=(),#(512, 256, 512),
                                                                    train=Train.WEIGHTS,
                                                                    gamma=.3,
                                                                    lr=1e-2
                                                                    )
        
        self.abstract_space_blas.input = self.abstract_space_rules.choice.main

        self.abstract_space_rules.rules.lhs.bu.input = self.abstract_construction_input.main

        self.abstract_space_pool["abstract_space_rules.rules"] = (
            self.abstract_space_rules.rules.main,
            lambda d: d.shift(x=1).scale(x=0.5).logit())
        
        self.abstract_space_pool["abstract_space_blas"] = (
            self.abstract_space_blas.main,
            lambda d: d.bound_min(x=1e-8).log().with_default(c=0.0))
        
        self.abstract_space_pool["abstract_space_matchstats"] = (
            self.abstract_space_matchstats.main,
            lambda d: d.bound_min(x=1e-8).log().with_default(c=0.0))

        self.abstract_space_pool["search_space_netscores"] = (
            self.construction_net.olayer.main,
            lambda d: d.bound_min(x=1e-8).log().with_default(c=0.0)) # TODO: verify this scaling..
        
        self.abstract_space_rules.bla_main = self.abstract_space_pool.main
        
        self.abstract_space_rules.choice.input = self.abstract_space_pool.main

        
        self.abstract_space_choice.input = self.abstract_space_rules.rules.rhs.td.main

        with self.abstract_space_pool.params[0].mutable():
            self.abstract_space_pool.params[0][~self.abstract_space_pool.p["blas"]] = 2e-1
        
        #backtracking queues: #TODO: better way to do this is probably with Sites, adn their inbuilt deque
        self.past_constructions = []
        self.past_chosen_rules = []
        self.past_chosen_rules_abstract = []
        self.all_rule_history = []
        self.all_rule_history_abstract = []

        #RL stats
        self.construction_reward_vals = []
        self.construction_qvals = []
        self.construction_net_training_results = []

        self.search_space_trigger_wait = [self.search_space_pool.update, self.abstract_search_space_pool.update]

    def resolve(self, event: Event) -> None:
        super().resolve(event)

        # ABSTRACT SEARCH PROCESSING
        if event.source == self.abstract_space_rules.rules.update:
            self.abstract_space_blas.update()
            self.abstract_space_matchstats.update()
        
        elif event.source == self.abstract_space_pool.update and all(e.source != self.abstract_space_pool.update for e in self.system.queue):
            self.abstract_space_rules.trigger()
        
        elif event.source == self.abstract_space_rules.rules.rhs.td.update:
            self.abstract_space_choice.trigger()
        
        elif event.source == self.abstract_space_choice.select:
            cur_sample = self.abstract_space_rules.choice.sample
            cur_rule_choice = self.abstract_space_rules.choice.poll()
            cur_choice = self.abstract_space_choice.poll()

            if cur_choice[~self.abstract_space.io.stop * ~self.abstract_space.response] == ~self.abstract_space.io.stop * ~self.abstract_space.response.yes:
                self.end_construction()
                self.response_input.send(self.search_space_choice.main[0]) # send the choice to the response input -- to make a decision out of 
            else:
                self.past_chosen_rules_abstract.append(cur_sample[0][list(cur_rule_choice.values())[0]])
                self.all_rule_history_abstract.append(cur_sample[0][list(cur_rule_choice.values())[0]])
                self.construction_input.send(self.abstract_space_choice.main[0]) # #TODO: does this add or replace?
        
        elif self.abstract_space_matchstats.increment:
            # make the mask zero:
            new_empty_mask = self.abstract_space_matchstats.cond.new({}).with_default(c=0.0)
            self.abstract_space_matchstats.cond.data.pop()
            self.abstract_space_matchstats.cond.data.append(new_empty_mask)
            self.abstract_space_matchstats.discount()
        
        elif event.source == self.search_space_matchstats.increment:
            # make the mask zero:
            new_empty_mask = self.search_space_matchstats.cond.new({}).with_default(c=0.0)
            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.cond.data.append(new_empty_mask)
            self.search_space_matchstats.discount()#TODO: apt timedelta?

        elif event.source == self.construction_net.error.update:
            self.construction_net_training_results.append(self.construction_net.error.main[0].pow(x=2.0))

    @override
    def resolve_lowlevel_search_choice(self, event: Event) -> None:
        #check if indeed we need to stop construction, if triggered the STOP rule
        cur_sample = self.search_space_rules.choice.sample
        cur_rule_choice = self.search_space_rules.choice.poll()
        
        temp_sample = cur_sample.new(cur_sample[0]._d).with_default(c=-math.inf)
        temp_sample = temp_sample.exp().div(temp_sample.exp().sum())
        cur_sample.data.pop()
        cur_sample.data.append(temp_sample) # simple copy for softmaxing activation

        cur_choice = self.search_space_choice.poll()

        # change this score from 0.2 to something else more representative of the fact that an upper level rule constrained things
        if cur_sample[0][list(cur_rule_choice.values())[0]] < 0.2: #backtrack # TODO: guaranteed to be list of size 1 yea?
            new_rule_mask = self.search_space_matchstats.cond.new({list(cur_rule_choice.values())[0]: 1.0}).with_default(c=0.0)
            new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=0.0)#we want to increment the negativity count
            
            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.crit.data.pop()

            self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition ot only change scores for this rule
            self.search_space_matchstats.crit.data.append(new_crit_score) 

            self.search_space_matchstats.increment() # TODO: apt timedelta?
            last_construction = self.past_constructions.pop()
            self.construction_input.send(last_construction) # pop the last construction
            self.mlp_construction_input.send(mlpify(last_construction, self.mlp_construction_input.main.index))

            # also give -1 reward to the rule that was chosen 
            self.construction_net.error.send({list(cur_rule_choice.values())[0]: -1.0}) # TODO: check this
            self.construction_reward_vals.append(-1.0)
            self.construction_qvals.append(self.search_space_pool["search_space_netscores"][0].max().c)

        elif cur_choice[~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens] == ~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens.stop_construction: # TODO: check this
            self.end_construction()
            self.response_input.send(self.search_space_choice.main[0]) # send the choice to the response input -- to make a decision out of 
        else: #continue construction
            self.past_constructions.append(self.search_space_choice.main[0])
            self.past_chosen_rules.append(cur_sample[0][list(cur_rule_choice.values())[0]])
            self.all_rule_history.append(cur_sample[0][list(cur_rule_choice.values())[0]])
            self.construction_input.send(self.search_space_choice.main[0]) # loop it back in --for more selections
            self.mlp_construction_input.send(mlpify(self.search_space_choice.main[0], self.mlp_construction_input.main.index)) # TODO: check this

    @override
    def start_construct_trial(self, 
        dt: timedelta, 
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        # the previous construction trial has ended, so clear TD trackers
        self.construction_net.error.reward.data.clear() # TODO: anyway to schedule such changes than doing it here?
        self.construction_net.error.qvals.data.clear()
        self.construction_net.error.action.data.clear()

        #add new 0-default entries
        self.construction_net.error.reward.data.append(self.construction_net.error.reward.new({}).with_default(c=0.0))
        self.construction_net.error.qvals.data.append(self.construction_net.error.qvals.new({}).with_default(c=0.0))
        self.construction_net.error.action.data.append(self.construction_net.error.action.new({}).with_default(c=0.0))
        

        self.system.schedule(self.start_construct_trial, dt=dt, priority=priority)
    
    @override
    def propagate_feedback(self, 
                           dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION,
                           correct:float = 0) -> None:
        
        for rule in self.past_chosen_rules:
            new_rule_mask = self.search_space_matchstats.cond.new({rule: 1.0}).with_default(c=0.0)
            new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=correct)

            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.crit.data.pop()

            self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition to only change scores for this rule
            self.search_space_matchstats.crit.data.append(new_crit_score)
            
            self.search_space_matchstats.increment() # TODO: apt timedelta?
            self.search_space_matchstats.discount()
            self.schedule(self.propagate_feedback, dt=dt, priority=priority)

            #update similarly the construction net
            self.construction_net.error.send({rule: correct})
            self.construction_reward_vals.append(correct)
            self.construction_qvals.append(self.search_space_pool["search_space_netscores"][0].max().c)
