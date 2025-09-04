from datetime import timedelta
from typing import override
from pprint import pprint
import math
import random

from tqdm import tqdm
import matplotlib.pyplot as plt
from pyClarion import (
    Input,
    Choice,
    Agent,
    Event,
    Priority,
    Family,
    BaseLevel,
    Pool,
    NumDict,
    Key,
)
from pyClarion.components.stats import MatchStats


from utils import (
    mlpify,
    filter_keys_by_rule_chunk,
    clean_construction_input,
    make_goal_outputs_construction_input,
    goal_shape_extractor,
    make_response_input,
    check_construction_input_match
)
from pyc_utils import RuleWBLA, FlippableInput
from knowledge_init import (
    BrickConstructionTask,
    BrickResponseTask,
    BrickConstructionTaskAbstractParticipant,
    Numbers,
    HighLevelConstructionSignals,
    JustYes,
    MLPConstructionIO,
)
from q_learning import external_mlp_handle, BATCH_SIZE

EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 15000 #120 b1

GREEDY_MOVES = []

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

    p: Family
    e: Family

    past_constructions: list
    past_chosen_rules: list
    past_chosen_rule_lhs_history: list
    past_chosen_rule_choices: list
    all_rule_history: list
    all_rule_lhs_history: list
    all_constructions: list

    def __init__(self, name: str, **kwargs) -> None:
        p = Family()
        e = Family()

        r_construction = Family()  # rule family for construction rules
        r_response = Family()  # rule family for response rules
        c_construction = Family()  # construction family for construction chunks
        c_response = Family()  # response family for response chunks

        response_space = BrickResponseTask()
        construction_space = kwargs.get(
            "construction_space", BrickConstructionTask()
        )  # default to the construction space
        if "construction_space" in kwargs:
            del kwargs["construction_space"]

        super().__init__(
            name,
            p=p,
            e=e,
            construction_space=construction_space,
            response_space=response_space,
            r_construction=r_construction,
            r_response=r_response,
            c_construction=c_construction,
            c_response=c_response,
            **kwargs,
        )
        self.p = p
        self.e = e
        self.response_space = response_space
        self.construction_space = construction_space

        with self:
            self.construction_input = FlippableInput(
                "construction_input",
                (construction_space, construction_space),
                reset=False,
            )
            self.response_input = FlippableInput(
                "response_input", (response_space, response_space), reset=True
            )

            self.response_rules = RuleWBLA(
                "response_rules",
                p=p,
                r=r_response,
                c=c_response,
                d=response_space,
                v=response_space,
                sd=1e-4,
            )
            self.search_space_rules = RuleWBLA(
                "search_space_rules",
                p=p,
                r=r_construction,
                c=c_construction,
                d=construction_space,
                v=construction_space,
                sd=1e-4,
            )

            self.search_space_matchstats = MatchStats(
                "search_space_matchstats",
                p,
                self.search_space_rules.rules.rules,
                th_cond=0.9,
                th_crit=0.9,
            )  # 0.9 because i want to compare against 1.

            self.response_pool = Pool(
                "pool", p, self.response_rules.rules.rules, func=NumDict.sum
            )  # to pool together the blas and condition activations
            self.search_space_pool = Pool(
                "search_space_pool",
                p,
                self.search_space_rules.rules.rules,
                func=NumDict.sum,
            )  # similar function

            self.response_choice = Choice(
                "choice", p, (response_space, response_space), sd=1e-2
            )
            self.search_space_choice = Choice(
                "search_space_choice",
                p,
                (construction_space, construction_space),
                sd=1e-2,
            )

        self.response_rules.rules.lhs.bu.input = self.response_input.main
        self.search_space_rules.rules.lhs.bu.input = self.construction_input.main

        self.search_space_pool["search_spaces_rules.rules"] = (
            self.search_space_rules.rules.main,
            lambda d: d.shift(x=1).scale(x=0.5).logit(),
        )
        self.response_pool["response_rules.rules"] = (
            self.response_rules.rules.main,
            lambda d: d.shift(x=1).scale(x=0.5).logit(),
        )  # you can take atmost 0.2 points of activation off using matchstats

        self.search_space_pool["search_space_matchstats"] = (
            self.search_space_matchstats.main,
            lambda d: d.shift(x=1).tanh().scale(x=0.2),
        )

        self.response_rules.bla_main = (
            self.response_pool.main
        )  # updated site for the response rules to take BLAS into account
        self.search_space_rules.bla_main = self.search_space_pool.main
        # rewire choice input
        self.search_space_rules.choice.input = self.search_space_pool.main
        self.response_rules.choice.input = self.response_pool.main

        self.response_choice.input = self.response_rules.rules.rhs.td.main  # bu choice
        self.search_space_choice.input = self.search_space_rules.rules.rhs.td.main

        # backtracking queues:
        self.past_constructions = []
        self.past_chosen_rules = []
        self.past_chosen_rule_choices = []
        self.past_chosen_rule_lhs_history = []
        self.all_rule_history = []
        self.all_rule_lhs_history = []
        self.all_constructions = []

        # wait events for low level pool update;
        self.search_space_trigger_wait = []
        self.response_trigger_wait = []
        self.construction_input_wait = []

        self.trigger_response = False

        self.training= True

    def resolve(self, event: Event) -> None:
        # -- RESPONSE PROCESSING --
        if (
            event.source == self.response_pool.update
            and self.trigger_response
            and all(
                e.source not in self.response_trigger_wait for e in self.system.queue
            )
        ):
            self.response_rules.trigger()
        elif event.source == self.response_rules.rules.rhs.td.update:
            self.response_choice.trigger()  # poll outside the loop in experimental loop
        elif event.source == self.start_response_trial:
            self.trigger_response = True

        # -- SEARCH PROCESSING --
        elif event.source == self.start_construct_trial:
            self.trigger_response = False
        elif event.source == self.construction_input.send and (
            any(e.source in self.construction_input_wait for e in self.system.queue)
            or not self.construction_input_wait
        ):
            self.past_constructions.append(
                self.construction_input.main[0].d.copy()
            )  # add the current construction to the past constructions
            self.all_constructions.append(
                self.construction_input.main[0].d.copy()
            )  # add the current construction to the all constructions
        elif event.source == self.search_space_rules.rules.update:
            self.search_space_matchstats.update()  # update the match stats
        elif event.source == self.search_space_pool.update and all(
            e.source not in self.search_space_trigger_wait for e in self.system.queue
        ):
            self.search_space_rules.trigger()
        elif event.source == self.search_space_rules.rules.rhs.td.update:
            self.search_space_choice.trigger()
        elif event.source == self.search_space_choice.select:
            self.resolve_lowlevel_search_choice(event)
        elif event.source == self.search_space_matchstats.increment:
            # make the mask zero:
            new_empty_mask = self.search_space_matchstats.cond.new(
                {}).with_default(c=0.0)
            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.cond.data.append(new_empty_mask)
            self.search_space_matchstats.discount()
        elif event.source == self.search_space_matchstats.discount and any(
            e.source == self.end_construction_feedback for e in self.system.queue
        ):
            self.propagate_feedback()
        elif event.source == self.end_construction:
            # clear system queue
            # at this point, you should have a clear target_grid representation
            # built -- correct or incorrect
            self.system.queue.clear()

    def toggle_training(self):
        self.training = not self.training
        return self.training

    def modify_matchstats(self, past_rule_choice, pm=False) -> None:
        new_rule_mask = self.search_space_matchstats.cond.new(
            {list(past_rule_choice.values())[0]: 1.0}
        ).with_default(c=0.0)
        new_crit_score = self.search_space_matchstats.crit.new({}).with_default(
            c=0.0 if not pm else 1.0
        )  # we want to increment the negativity count

        self.search_space_matchstats.cond.data.pop()
        self.search_space_matchstats.crit.data.pop()

        self.search_space_matchstats.cond.data.append(
            new_rule_mask
        )  # update the condition ot only change scores for this rule
        self.search_space_matchstats.crit.data.append(new_crit_score)

        self.search_space_matchstats.increment()

    def start_construct_trial(
        self, dt: timedelta, priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.system.schedule(
            self.start_construct_trial,
            dt=dt,
            priority=priority)

    def resolve_lowlevel_search_choice(self, event: Event) -> None:
        raise NotImplementedError

    def end_construction(
        self,
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION,
    ) -> None:
        self.system.schedule(self.end_construction, dt=dt, priority=priority)

    def end_construction_feedback(
        self,
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION,
    ) -> None:
        self.system.schedule(
            self.end_construction_feedback,
            dt=dt,
            priority=priority)

    def start_response_trial(
        self, dt: timedelta, priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.response_input.send(
            make_response_input(
                self.construction_input.main[0], self.response_input.main[0].i
            ).d
        )  # send the construction input to the response input
        self.system.schedule(
            self.start_response_trial,
            dt=dt,
            priority=priority)

    def finish_response_trial(
        self, dt: timedelta, priority: Priority = Priority.PROPAGATION
    ) -> None:
        self.past_constructions = []
        self.past_chosen_rules = []
        self.all_rule_history = []
        self.all_rule_lhs_history = []
        self.all_constructions = []
        self.past_chosen_rule_lhs_history = []

        self.system.queue.clear()

        self.system.schedule(
            self.finish_response_trial,
            dt=dt,
            priority=priority)

    def feedback(self, correct: float = 0) -> None:
        if not self.past_chosen_rule_choices:
            return

        rule = self.past_chosen_rule_choices.pop()
        # is there a correct already in there?:
        if self.search_space_matchstats.crit[0].c:
            correct = 1.0

        self.modify_matchstats(rule, pm=correct)

    def propagate_feedback(self, correct: float = 0) -> None:
        self.feedback(correct)


class LowLevelParticipant(BaseParticipant):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)

        self.search_space_trigger_wait = [self.search_space_pool.update]
        self.response_trigger_wait = [self.response_rules.rules.update]

    def resolve_lowlevel_search_choice(self, event):
        # check if indeed we need to stop construction, if triggered the STOP
        # rule
        cur_rule_choice = self.search_space_rules.choice.poll()
        cur_rule_number = list(cur_rule_choice.values())[0][-1:][0][0]

        cur_choice = self.search_space_choice.poll()

        if (
            cur_choice[
                ~self.construction_space.io.construction_signal
                * ~self.construction_space.signal_tokens
            ]
            == ~self.construction_space.io.construction_signal
            * ~self.construction_space.signal_tokens.backtrack_construction
        ):  # backtrack
            new_rule_mask = self.search_space_matchstats.cond.new(
                {list(cur_rule_choice.values())[0]: 1.0}
            ).with_default(c=0.0)
            new_crit_score = self.search_space_matchstats.crit.new(
                {}).with_default(c=0.0)  # we want to increment the negativity count

            self.search_space_matchstats.cond.data.pop()
            self.search_space_matchstats.crit.data.pop()

            self.search_space_matchstats.cond.data.append(
                new_rule_mask
            )  # update the condition ot only change scores for this rule
            self.search_space_matchstats.crit.data.append(new_crit_score)

            self.search_space_matchstats.increment()
            last_construction = self.past_constructions.pop()
            self.past_chosen_rule_lhs_history.pop()
            # pop the last construction, also make sure to reset: flip is false
            # as initialized with reset = false
            self.construction_input.send(last_construction, flip=True)

        elif (
            cur_choice[
                ~self.construction_space.io.construction_signal
                * ~self.construction_space.signal_tokens
            ]
            == ~self.construction_space.io.construction_signal
            * ~self.construction_space.signal_tokens.stop_construction
        ):
            self.end_construction()
        else:  # continue construction
            cur_additions = filter_keys_by_rule_chunk(
                self.search_space_rules.rules.rhs.chunks._members_[
                    Key(f"{cur_rule_number}")
                ],
                self.search_space_choice.main[0].d,
            )
            self.past_chosen_rules.append(cur_additions)
            self.all_rule_history.append(cur_additions)
            self.all_rule_lhs_history.append(
                self.search_space_rules.rules.lhs.chunks._members_[
                    Key(f"{cur_rule_number}")
                ]
            )
            self.past_chosen_rule_lhs_history.append(
                self.search_space_rules.rules.lhs.chunks._members_[
                    Key(f"{cur_rule_number}")
                ]
            )
            self.construction_input.send(
                cur_additions
            )  # loop it back in --for more selections


class AbstractParticipant(BaseParticipant):
    """
    Contains everything the non-abstract participant does with the added features:
    1. RL and MLP is now over the ryles
    2. there is an abstract rule space -- with choices, and pools over the same
    3. A choice in the abstract space leads to a downstream impact on the construction space
    4. This downstream impact influences activations of low-level construction choices
    5. Which prgoresses by way of rule activations, blas, and math statistics
    """

    def __init__(self, name: str, layers: int) -> None:
        r_abstract = Family()  # rule family for abstract rules
        c_abstract = Family()  # abstract family for abstract chunks

        construction_space = BrickConstructionTaskAbstractParticipant()
        # RL components:
        h = Family()
        mlp_space_1 = MLPConstructionIO()
        mlp_space_2 = Numbers()
        mlp_output_space_1 = HighLevelConstructionSignals()
        mlp_output_space_2 = JustYes()

        super().__init__(
            name,
            h=h,
            construction_space=construction_space,
            r_abstract=r_abstract,
            c_abstract=c_abstract,
            mlp_space_1=mlp_space_1,
            mlp_space_2=mlp_space_2,
            mlp_output_space=mlp_output_space_1,
            mlp_output_space_2=mlp_output_space_2,
        )

        self.mlp_space_1 = mlp_space_1
        self.mlp_space_2 = mlp_space_2
        self.mlp_output_space_1 = mlp_output_space_1
        self.mlp_output_space_2 = mlp_output_space_2

        with self:
            self.mlp_construction_input = FlippableInput(
                "mlp_construction_input", (mlp_space_1, mlp_space_2), reset=False)
            self.abstract_goal_choice = Choice(
                "abstract_goal_choice",
                self.p,
                (mlp_output_space_2, mlp_output_space_1),
                sd=1e-10,
            )

        # MLP SETUP:
        (
            self.goal_net,
            self.goal_net_memory,
            self.goal_net_update,
            self.goal_net_optimize,
        ) = external_mlp_handle(
            state_keys=[k for k in self.mlp_construction_input.main[0]],
            action_keys=[k for k in self.abstract_goal_choice.main[0]],
            layers=layers
        )

        # extra backtracking queues:
        self.past_chosen_goals = []
        self.all_goal_history = []

        # RL stats
        self.construction_reward_vals = []
        self.construction_qvals = []
        self.construction_net_training_results = []

        self.transition_store = []

        self.search_space_trigger_wait = [
            self.search_space_pool.update,
            self.shift_goal,
        ]
        self.response_trigger_wait = [self.response_rules.rules.update]
        self.construction_input_wait = [self.shift_goal]

        self.backtracks = 0

    def resolve(self, event: Event) -> None:
        super().resolve(event)

        # ABSTRACT SEARCH PROCESSING
        if event.source == self.mlp_construction_input.send:
            self.shift_goal()
        elif event.source == self.shift_goal and len(self.transition_store) > 0:
            self.transition_store.insert(
                2, self.mlp_construction_input.main[0].d.copy()
            )
            if check_construction_input_match(self.mlp_construction_input.main.data[0].d):
                self.transition_store[-1] = 1.0 #construction is correct and its over
                self.construction_reward_vals[-1] = 1.0
            self.backward_qnet()
        elif event.source == self.shift_goal:
            self.forward_qnet()
            self.transition_store = [
                self.mlp_construction_input.main[0].d.copy()]
        elif event.source == self.backward_qnet and not any(
            e.source == self.end_construction_feedback for e in self.system.queue
        ):
            if check_construction_input_match(self.mlp_construction_input.main.data[0].d):
                self.end_construction()
            else:
                # run the q_net on the new stuff
                self.forward_qnet()
                self.transition_store = [
                    self.mlp_construction_input.main[0].d.copy()]
        elif event.source == self.forward_qnet:
            # at this point olayer.forward has been applied
            self.abstract_goal_choice.trigger()
        elif event.source == self.abstract_goal_choice.select:
            cur_choice = self.abstract_goal_choice.poll()
            greedy_move = self.select_action()
            GREEDY_MOVES.append(int(greedy_move))
            plt.plot(GREEDY_MOVES)
            plt.savefig("data/figures/random.png")
            if not greedy_move:
                if len(self.past_constructions) == 1:
                    # first move 80% starts 20 % random
                    cur_choice = {
                        c: random.choices(
                            [k for k in self.abstract_goal_choice.main[0]],
                            [0.2] * 4 + [0.2 / 48] * 48,
                        )[0]
                        for c in cur_choice
                    }
                else:
                    # opposite
                    cur_choice = {
                        c: random.choices(
                            [k for k in self.abstract_goal_choice.main[0]],
                            [0.03 / 4] * 4 + [0.97 / 48] * 48,
                        )[0]
                        for c in cur_choice
                    }

            self.past_chosen_goals.append(
                str(list(cur_choice.values())[0][-1][0]))
            self.all_goal_history.append(
                goal_shape_extractor(str(list(cur_choice.values())[0][-1][0]))
            )
            self.transition_store.append(list(cur_choice.values())[0])
            self.construction_input.send(
                make_goal_outputs_construction_input(
                    self.construction_input.main[0], cur_choice
                ),
                flip=True,
            )

    def resolve_lowlevel_search_choice(self, event):
        # check if indeed we need to stop construction, if triggered the STOP
        # rule
        cur_rule_choice = self.search_space_rules.choice.poll()
        cur_rule_number = list(cur_rule_choice.values())[0][-1:][0][0]

        cur_choice = self.search_space_choice.poll()

        if (
            self.backtracks > 15
        ):
            self.end_construction()
        elif (
            cur_choice[
                ~self.construction_space.io.construction_signal
                * ~self.construction_space.signal_tokens
            ]
            == ~self.construction_space.io.construction_signal
            * ~self.construction_space.signal_tokens.backtrack_construction
        ):  # backtrack
            if (
                self.past_chosen_rule_lhs_history
            ):  # this rule is not to blame, but the previous is
                past_rule_choice = self.past_chosen_rule_choices.pop()

                # self.modify_matchstats(past_rule_choice, pm=False)

                self.past_chosen_rule_lhs_history.pop()
                self.past_chosen_rules.pop()
                self.past_chosen_goals.pop()

            if len(self.past_constructions) == 1:
                # not a right start rule
                self.all_goal_history.pop()

            # -- MLP ACTIONS --
            # one bad reward for the last choice
            self.construction_reward_vals.append(-0.1)
            self.construction_qvals.append(
                self.abstract_goal_choice.input[0].max().c)

            last_construction = self.past_constructions.pop()

            self.transition_store.append(-0.1)

            self.mlp_construction_input.send(
                mlpify(last_construction), flip=True)
            # pop the last construction, also make sure to reset: flip is false
            # as initialized with reset = false
            self.construction_input.send(
                clean_construction_input(last_construction), flip=True)
            self.backtracks += 1

        elif (
            cur_choice[
                ~self.construction_space.io.construction_signal
                * ~self.construction_space.signal_tokens
            ]
            == ~self.construction_space.io.construction_signal
            * ~self.construction_space.signal_tokens.stop_construction
        ):
            self.end_construction()
        elif len(self.past_chosen_rules) > 5:
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
            self.mlp_construction_input.send(
                mlpify(last_construction), flip=True)
            self.construction_input.send(
                clean_construction_input(last_construction, leave_only_inputs=True),
                flip=True,
            )  # pop the last construction, also make sure to reset: flip is false as initialized with reset = false

            self.transition_store.append(-0.1)
            self.construction_reward_vals.append(-0.1)
            self.construction_qvals.append(
                self.abstract_goal_choice.input[0].max().c)
            self.backtracks += 1
        else:
            cur_additions = filter_keys_by_rule_chunk(
                self.search_space_rules.rules.rhs.chunks._members_[
                    Key(f"{cur_rule_number}")
                ],
                self.search_space_choice.main[0].d,
            )
            self.past_chosen_rules.append(cur_additions)
            self.all_rule_history.append(cur_additions)
            self.all_rule_lhs_history.append(
                self.search_space_rules.rules.lhs.chunks._members_[
                    Key(f"{cur_rule_number}")
                ]
            )
            self.past_chosen_rule_lhs_history.append(
                self.search_space_rules.rules.lhs.chunks._members_[
                    Key(f"{cur_rule_number}")
                ]
            )
            self.past_chosen_rule_choices.append(cur_rule_choice)

            self.mlp_construction_input.send(mlpify(cur_additions))
            self.construction_input.send(
                cur_additions
            )  # loop it back in --for more selections
            self.transition_store.append(-0.01)  # tiny punishment for timestep
            self.construction_reward_vals.append(-0.01) 
            self.construction_qvals.append(
                self.abstract_goal_choice.input[0].max().c)

    def modify_matchstats(self, past_rule_choice, pm=False):
        if self.select_action():
            super().modify_matchstats(past_rule_choice, pm)

    @override
    def propagate_feedback(self, correct=0):
        # self.feedback(correct == 1)
        # feedback for the MLP
        self.transition_store.append(None)
        self.transition_store.append(-1.0 if not correct else correct)
        self.backward_qnet()
        self.construction_reward_vals.append(-1.0 if not correct else correct)
        self.construction_qvals.append(
            self.abstract_goal_choice.input[0].max().c)

    def shift_goal(
        self,
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.DEFERRED,
    ) -> None:
        self.system.schedule(self.shift_goal, dt=dt, priority=priority)

    def forward_qnet(
        self,
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION,
    ) -> None:
        out_actions = self.goal_net.forward(
            self.mlp_construction_input.main[0].d)

        # outs = sorted(out_actions.items(), key=lambda x: x[1], reverse=True)
        # p = lambda x: math.exp(x)/sum(math.exp(s) for _, s in outs)
        # pprint([(str(k).split(":")[-1], p(v)) for k,v in outs][:5])
        # print("Entropy Baseline: ", -sum(math.log(1/len(outs))/len(outs) for _, x in outs))
        # print("Entropy: ", -sum(p(x)*math.log(p(x)) for _, x in outs))
        self.system.schedule(
            self.forward_qnet,
            self.abstract_goal_choice.input.update(out_actions),
            dt=dt,
            priority=priority,
        )

    def backward_qnet(
        self,
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.LEARNING,
    ) -> None:

        if self.training:
            loss = self.goal_net_optimize(use_memory=False,
                                        **{["state",
                                            "action",
                                            "next_state",
                                            "reward"][i]: self.transition_store[i] for i in range(4)},
                                        )

            self.construction_net_training_results.append(loss)
            # push into memory buffer
            self.goal_net_memory.push(self.goal_net_memory.positive_memory if self.transition_store[-1] == 1.0 else self.goal_net_memory.negative_memory, *self.transition_store)
            self.goal_net_update()
        self.system.schedule(self.backward_qnet, dt=dt, priority=priority)

    def replay_optimize_qnet(
        self,
        dt: timedelta = timedelta(seconds=0),
        priority: Priority = Priority.PROPAGATION,
    ) -> None:
        if self.training:
            for _ in tqdm(range(max(50, (20*len(self.goal_net_memory))//(BATCH_SIZE)))):
                loss = self.goal_net_optimize(use_memory=True)
                self.construction_net_training_results.append(loss)
                self.goal_net_update()
        self.system.schedule(
            self.replay_optimize_qnet,
            dt=dt,
            priority=priority)

    def select_action(self):
        if not self.training: return True
        steps_done = len(self.construction_net_training_results)+ 9000
        # if steps_done > EPS_DECAY:
        #     r_window = sum(self.construction_reward_vals[-10:])/10
        #     EPS_DECAY *= (0.88 + 1/(1+math.exp(2*(r_window - 1.0))))
        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(
            -1.0 * steps_done / EPS_DECAY
        )
        return sample > eps_threshold

    def finish_response_trial(
        self, dt: timedelta, priority: Priority = Priority.PROPAGATION
    ) -> None:
        super().finish_response_trial(dt=dt, priority=priority)
        self.past_chosen_goals = []
        self.all_goal_history = []
        self.past_chosen_rule_choices = []
        self.transition_store = []
        self.backtracks = 0

#total steps before convergence for block1: + 2500 + 1400 + 500