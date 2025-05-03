import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
from typing import List

from pyClarion import Key

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# code adapted from https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


def pyc_to_torch(d: dict[Key, float], indices=List[Key]):
    data_array = torch.zeros(len(indices))
    for k in d:
        i = indices.index(k)
        data_array[i] = d[k]
    return data_array

def torch_to_pyc(t: torch.Tensor, indices=List[Key]):
    data_dict = {}
    for i, k in enumerate(indices):
        data_dict[k] = t[i].item()
    return data_dict

class ReplayMemory(object):
    def __init__(self, capacity, state_keys, action_keys):
        self.memory = deque([], maxlen=capacity)
        self.state_keys = state_keys
        self.action_keys = action_keys

    def push(self, *args):
        #convert state action and next state to tensors
        state = pyc_to_torch(args[0], self.state_keys)
        action = torch.tensor([self.action_keys.index(args[1])])
        next_state = pyc_to_torch(args[2], self.state_keys) if args[2] is not None else None
        self.memory.append(Transition(state, action, next_state, torch.tensor([args[3]], dtype=torch.float32)))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)
    
    def __len__(self):
        return len(self.memory)
    

class DQN(nn.Module):
    def __init__(self, state_keys, action_keys):
        super(DQN, self).__init__()

        n_observations = len(state_keys)
        n_actions = len(action_keys)
        self.fc1 = nn.Linear(n_observations, 128)
        self.fc2 = nn.Linear(128, 256)
        self.fc3 = nn.Linear(256, 128)
        self.fc4 = nn.Linear(128, n_actions)

        self.observation_keys = state_keys
        self.action_keys = action_keys

    def forward(self, x):
        if type(x) is not dict:
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = F.relu(self.fc3(x))
            x = self.fc4(x)
        else:
            with torch.no_grad():
                x = pyc_to_torch(x, indices=self.observation_keys)
                x = self.forward(x)
                x = torch_to_pyc(x, indices=self.action_keys)
        return x

BATCH_SIZE = 64
GAMMA = 0.9
TAU = 0.005
LR = 1e-3
ACTIONS = list(range(52))

def external_mlp_handle(state_keys, action_keys):
    device = torch.device("cpu")

    policy_net = DQN(state_keys, action_keys)
    target_net = DQN(state_keys, action_keys)
    target_net.load_state_dict(policy_net.state_dict())

    optimizer = optim.Adam(policy_net.parameters(), lr=LR)
    memory = ReplayMemory(10000,
                          state_keys=state_keys,
                          action_keys=action_keys)

    def optimize_model(use_memory=True, # during trial -- no replay buffer, during rest in bw sessions - yes 
                    state=None, action=None, next_state=None, reward=None):
        if use_memory:
            if len(memory) < BATCH_SIZE:
                batch_size = len(memory)
            else:
                batch_size = BATCH_SIZE
            transitions = memory.sample(batch_size)
            # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
            # detailed explanation). This converts batch-array of Transitions
            # to Transition of batch-arrays.
            batch = Transition(*zip(*transitions))

            # Compute a mask of non-final states and concatenate the batch elements
            # (a final state would've been the one after which simulation ended)
            non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                                batch.next_state)), device=device, dtype=torch.bool)
            non_final_next_states = torch.stack([s for s in batch.next_state
                                                        if s is not None])
            state_batch = torch.stack(batch.state)
            action_batch = torch.stack(batch.action)
            reward_batch = torch.stack(batch.reward)
        else:
            assert state is not None and action is not None and reward is not None
            batch_size = 1

            state = pyc_to_torch(state, state_keys)
            action = [action_keys.index(action)]
            next_state = pyc_to_torch(next_state, state_keys) if next_state is not None else None
            
            state_batch = state.unsqueeze(0)
            action_batch = torch.tensor(action, device=device).unsqueeze(0)
            reward_batch = torch.tensor([reward], device=device).unsqueeze(0)
            non_final_mask = torch.tensor([next_state is not None], device=device, dtype=torch.bool)
            non_final_next_states = next_state.unsqueeze(0) if next_state is not None else torch.tensor([], device=device).unsqueeze(0)

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(batch_size, device=device)
        with torch.no_grad():
            if torch.any(non_final_mask):
                next_state_values[non_final_mask] = target_net(non_final_next_states).max(1).values
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * GAMMA).unsqueeze(1) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values)

        # Optimize the model
        optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
        optimizer.step()

        return loss.item()

    def soft_update():
        target_net_state_dict = target_net.state_dict() 
        policy_net_state_dict = policy_net.state_dict()

        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key] * TAU + \
                                          target_net_state_dict[key] * (1.0 - TAU)
        target_net.load_state_dict(target_net_state_dict)
    
    return policy_net, memory, soft_update, optimize_model


