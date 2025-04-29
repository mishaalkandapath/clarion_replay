from pyClarion import Input, Choice, Agent, Event, Priority, Family, Atoms, Atom, BaseLevel, Pool, NumDict, Train, IDN
from pyClarion.components.stats import MatchStats


from utils import *
from knowledge_init import *
from q_learning import *

from datetime import timedelta
import math
import random

EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000

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
            lambda d: d.shift(x=1).tanh().scale(x=0.2)) # TODO: is the function here correct?
        
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
        self.all_rule_lhs_history = []
        self.all_constructions = []
        self.past_chosen_rule_lhs_history = []

        #wait events for low level pool update;
        self.search_space_trigger_wait = []
        self.response_trigger_wait = []
        self.construction_input_wait = []

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
        elif event.source == self.construction_input.send \
            and any(e.source in self.construction_input_wait for e in self.system.queue):
            self.past_constructions.append(self.construction_input.main[0].d.copy()) # add the current construction to the past constructions    
            self.all_constructions.append(self.construction_input.main[0].d.copy()) # add the current construction to the all constructions
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

    def modify_matchstats(self, past_rule_choice, pm=False) -> None:
        new_rule_mask = self.search_space_matchstats.cond.new({list(past_rule_choice.values())[0]: 1.0}).with_default(c=0.0)
        new_crit_score = self.search_space_matchstats.crit.new({}).with_default(c=0.0 if not pm else 1.0)#we want to increment the negativity count
        
        self.search_space_matchstats.cond.data.pop()
        self.search_space_matchstats.crit.data.pop()

        self.search_space_matchstats.cond.data.append(new_rule_mask) # update the condition ot only change scores for this rule
        self.search_space_matchstats.crit.data.append(new_crit_score) 

        self.search_space_matchstats.increment() # TODO: apt timedelta?
    
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

    def feedback(self, correct: float=0) -> None:
        if not self.past_chosen_rules:
            return
        
        rule = self.past_chosen_rules.pop()
        #is there a correct already in there?:
        if self.search_space_matchstats.crit[0].c:
            correct = 1.0

        self.modify_matchstats(rule, pm=correct)

    def propagate_feedback(self, correct:float = 0) -> None:
        self.feedback(correct)

class LowLevelParticipant(BaseParticipant):  

    def __init__(self, name: str) -> None:
        super().__init__(name=name)

        self.search_space_trigger_wait = [self.search_space_pool.update]
        self.response_trigger_wait = [self.response_rules.rules.update]

    def resolve_lowlevel_search_choice(self, event):
        #check if indeed we need to stop construction, if triggered the STOP rule
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
            self.past_chosen_rule_lhs_history.pop()
            self.construction_input.send(last_construction, flip=True) # pop the last construction, also make sure to reset: flip is false as initialized with reset = false

        elif cur_choice[~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens] == ~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens.stop_construction:
            self.end_construction() # TODO: consider adding stop construction rules to rule history for matchstats
        else: #continue construction
            # self.past_chosen_rules.append(list(cur_rule_choice.values())[0])
            # self.all_rule_history.append(list(cur_rule_choice.values())[0])
            cur_additions = filter_keys_by_rule_chunk(self.search_space_rules.rules.rhs.chunks._members_[Key(f"{cur_rule_number}")], self.search_space_choice.main[0].d)
            self.past_chosen_rules.append(cur_additions)
            self.all_rule_history.append(cur_additions)
            self.all_rule_lhs_history.append(self.search_space_rules.rules.lhs.chunks._members_[Key(f"{cur_rule_number}")])
            self.past_chosen_rule_lhs_history.append(self.search_space_rules.rules.lhs.chunks._members_[Key(f"{cur_rule_number}")])
            self.construction_input.send(cur_additions) # loop it back in --for more selections

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
        #RL components:
        h = Family()
        mlp_space_1 = MLPConstructionIO()
        mlp_space_2 = Numbers()
        mlp_output_space_1 = HighLevelConstructionSignals()
        mlp_output_space_2 = JustYes()

        super().__init__(name,
                         h=h,
                         construction_space=construction_space,
                         r_abstract=r_abstract,
                         c_abstract=c_abstract,
                         mlp_space_1=mlp_space_1, mlp_space_2=mlp_space_2,
                         mlp_output_space=mlp_output_space_1, mlp_output_space_2=mlp_output_space_2)
        
        self.mlp_space_1 = mlp_space_1
        self.mlp_space_2 = mlp_space_2
        self.mlp_output_space_1 = mlp_output_space_1
        self.mlp_output_space_2 = mlp_output_space_2

        with self:

            self.mlp_construction_input = FlippableInput("mlp_construction_input", (mlp_space_1, mlp_space_2), reset=False)
            self.abstract_goal_choice = Choice("abstract_goal_choice", self.p, (mlp_output_space_2, mlp_output_space_1), sd=1e-2)

        # MLP SETUP:
        self.goal_net, self.goal_net_memory, self.goal_net_update, self.goal_net_optimize = external_mlp_handle(
            state_keys= [k for k in self.mlp_construction_input.main[0]],
            action_keys = [k for k in self.abstract_goal_choice.main[0]]
        )
        
        #extra backtracking queues: #TODO: better way to do this is probably with Sites, adn their inbuilt deque
        self.past_chosen_goals = []
        self.all_goal_history = []

        self.past_chosen_rule_choices = []

        #RL stats
        self.construction_reward_vals = []
        self.construction_qvals = []
        self.construction_net_training_results = []
        
        self.transition_store = []

        self.search_space_trigger_wait = [self.search_space_pool.update, self.shift_goal]
        self.response_trigger_wait = [self.response_rules.rules.update]
        self.construction_input_wait = [self.shift_goal]

    def resolve(self, event: Event) -> None:
        super().resolve(event)

        # ABSTRACT SEARCH PROCESSING    
        if event.source == self.mlp_construction_input.send:
            self.shift_goal()
        elif event.source == self.shift_goal and len(self.transition_store) > 0:
                self.transition_store.insert(2, self.mlp_construction_input.main[0].d.copy())
                self.backward_qnet()
        elif event.source == self.shift_goal:
            self.forward_qnet()
            self.transition_store = [self.mlp_construction_input.main[0].d.copy()] 

        elif event.source == self.backward_qnet and all(e.source == self.end_construction_feedback for e in self.system.queue):
            # run the q_net on the new stuff
            self.forward_qnet()
            self.transition_store = [self.mlp_construction_input.main[0].d.copy()] 
        elif event.source == self.forward_qnet:
            self.abstract_goal_choice.trigger() # at this point olayer.forward has been applied
        elif event.source == self.abstract_goal_choice.select:
            cur_choice = self.abstract_goal_choice.poll()

            greedy_move = self.select_action()
            if not greedy_move:
                if len(self.past_constructions) == 1:
                    # first move 80% starts 20 % random
                    cur_choice = {c: random.choices([k for k in self.abstract_goal_choice.main[0]], [0.2]*4 + [0.2/48]*48)[0] for c in cur_choice} 
                else:
                    # opposite 80% others 20% start
                    cur_choice = {c: random.choices([k for k in self.abstract_goal_choice.main[0]], [0.03/4]*4 + [0.97/48]*48)[0] for c in cur_choice} 
                
            self.past_chosen_goals.append(cur_choice)
            self.transition_store.append(list(cur_choice.values())[0])
            self.construction_input.send(make_goal_outputs_construction_input(self.construction_input.main[0], cur_choice), flip=True)


    def resolve_lowlevel_search_choice(self, event):
        #check if indeed we need to stop construction, if triggered the STOP rule
        cur_rule_choice = self.search_space_rules.choice.poll()
        cur_rule_number = list(cur_rule_choice.values())[0][-1:][0][0]

        cur_choice = self.search_space_choice.poll()

        if cur_choice[~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens] == ~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens.backtrack_construction: #backtrack
            
            if self.past_chosen_rule_lhs_history: # this rule is not to blame, but the previous is
                past_rule_choice = self.past_chosen_rule_choices.pop()

                self.modify_matchstats(past_rule_choice, pm=False)

                self.past_chosen_rule_lhs_history.pop()
                self.past_chosen_rules.pop()

            #-- MLP ACTIONS --
            # one bad reward for the last choice
            self.construction_reward_vals.append(-1.0)
            self.construction_qvals.append(self.abstract_goal_choice.input[0].max().c)

            last_construction = self.past_constructions.pop()

            self.transition_store.append(-1.0)

            self.mlp_construction_input.send(mlpify(last_construction, self.mlp_construction_input.main[0].i), flip=True)
            self.construction_input.send(clean_construction_input(last_construction), flip=True) # pop the last construction, also make sure to reset: flip is false as initialized with reset = false

        elif cur_choice[~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens] == ~self.construction_space.io.construction_signal * ~self.construction_space.signal_tokens.stop_construction:
            self.end_construction() # TODO: consider adding stop construction rules to rule history for matchstats
        elif len(self.past_chosen_rules) > 4:
                # one too many -- restart --
                self.past_chosen_rules = []
                self.all_rule_history = []
                self.all_rule_lhs_history = []
                self.past_chosen_rule_lhs_history = []
                self.past_chosen_rule_choices = []
                self.past_chosen_goals = []
                self.all_goal_history = []
                self.past_constructions = [self.past_constructions[0]]

                last_construction = self.past_constructions.pop()
                self.mlp_construction_input.send(mlpify(last_construction, self.mlp_construction_input.main[0].i), flip=True)
                self.construction_input.send(clean_construction_input(last_construction, leave_only_inputs=True), flip=True) # pop the last construction, also make sure to reset: flip is false as initialized with reset = false

                self.transition_store.append(-1.0)

                self.construction_reward_vals.append(-1.0)
                self.construction_qvals.append(self.abstract_goal_choice.input[0].max().c)

                #TODO: matchstat updates?

        else:

            cur_additions = filter_keys_by_rule_chunk(self.search_space_rules.rules.rhs.chunks._members_[Key(f"{cur_rule_number}")], self.search_space_choice.main[0].d)
            self.past_chosen_rules.append(cur_additions)
            self.all_rule_history.append(cur_additions)
            self.all_rule_lhs_history.append(self.search_space_rules.rules.lhs.chunks._members_[Key(f"{cur_rule_number}")])
            self.past_chosen_rule_lhs_history.append(self.search_space_rules.rules.lhs.chunks._members_[Key(f"{cur_rule_number}")])
            self.past_chosen_rule_choices.append(cur_rule_choice)
            
            self.mlp_construction_input.send(mlpify(cur_additions, self.mlp_construction_input.main[0].i)) 
            self.construction_input.send(cur_additions) # loop it back in --for more selections

            self.transition_store.append(-0.1) # tiny punishment for timestep

    def modify_matchstats(self, past_rule_choice, pm=False):
        if self.select_action():
            super().modify_matchstats(past_rule_choice, pm)

    @override
    def propagate_feedback(self, correct = 0):
        self.feedback(correct)
        # feedback for the MLP
        self.transition_store.append(None)
        self.transition_store.append(-1.0 if not correct else 1.0)
        self.backward_qnet()

        self.construction_reward_vals.append(1.0 if correct else -1.0)
        self.construction_qvals.append(self.abstract_goal_choice.input[0].max().c)
    
    def shift_goal(self, 
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.DEFERRED
    ) -> None:
        self.system.schedule(self.shift_goal, dt=dt, priority=priority)


    # Qnet training
    def forward_qnet(self, 
                     dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        out_actions = self.goal_net.forward(self.mlp_construction_input.main[0].d)
        self.system.schedule(self.forward_qnet,
                             self.abstract_goal_choice.input.update(out_actions),
                             dt=dt, priority=priority)

    def backward_qnet(self, 
                     dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.LEARNING
    ) -> None:
        loss = self.goal_net_optimize(use_memory=False,
                               **{["state", "action", "next_state", "reward"][i]: self.transition_store[i] for i in range(4)})
        
        self.construction_net_training_results.append(loss)

        #push into memory buffer
        self.goal_net_memory.push(*self.transition_store)
        self.goal_net_update()
        self.system.schedule(self.backward_qnet,
                             dt=dt, priority=priority)

    def replay_optimize_qnet(self, 
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION
    ) -> None:
        for _ in range(5):
            loss = self.goal_net_optimize(use_memory=True)
            self.construction_net_training_results.append(loss)
            self.goal_net_update()

    def select_action(self):
        steps_done = len(self.construction_net_training_results)
        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * \
            math.exp(-1. * steps_done / EPS_DECAY)

        return sample > eps_threshold



"""
MLP will be changing the weights of the main in the input class -- by a certain amount
but ideally it should only change the weights of that which is already there. -- you can establish that by multiplication -- because if it isnt there, 
it is 0.

But what about the MLP -- it cant be an IDN with TD error. What do attention MLPs look like? Whats a good way to implement that?
"""

"""
Workflow:
1. send mlp inputs -- DONE
2. send construction_inputs -- DONE
3. forward mlp -- DONE
4. get mlp choice and pass it along to construction -- DONE
5. add new workign space to past constructions (NEED TO ADD AN MLP WAIT HERE) -- DONE
6. update rules and what not -- DONE
7. fire and choose a rule (NEED TO ADD AN MLP WAIT HERE) -- DONE
8. if a backtrack rule was chosen:
    -1 for the last two choices, propagate rewards - DONE
    pop the last construction, send it to MLP, continue -- DONE
9. otherwise, send the new construction to MLP, continue. -- DONE
10. repeat
11. at the end of the trial, if the construction was correct, make supposed changes to matchstats of low level rules, and propagate rewards to all the choices of the MLP in that right path

MLP WAIT has to disappear once olayer.forward has been applied. 

"""