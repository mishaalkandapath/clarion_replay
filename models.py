from collections import OrderedDict, Union, List

import torch
from torch import nn

from pyClarion import Key

def pyc_to_torch(d: dict[Union[Key, str], float],
                  indices=List[Union[Key, str]]):
    data_array = torch.zeros(len(indices))
    for k in d:
        i = indices.index(k)
        data_array[i] = d[k]
    return data_array


def torch_to_pyc(t: torch.Tensor, 
                 indices=List[Key]):
    data_dict = {}
    for i, k in enumerate(indices):
        data_dict[k] = t[i].item()
    return data_dict

class DQN(nn.Module):
    def __init__(self, state_keys, action_keys, n_layers=8):
        super().__init__()

        n_observations = len(state_keys)
        n_actions = len(action_keys)
        network = [("fc0", nn.Linear(n_observations, 128)),
                   ("rfc0", nn.ReLU())]
        assert n_layers%2 == 0, "Must be even number"
        last_num = 128
        for n_layer in range(n_layers):
                if n_layer < n_layers//2:
                    network.append((f"fc{n_layer+1}", 
                                    nn.Linear(last_num, 
                                              last_num*2)))
                    last_num = last_num * 2
                else:

                    network.append((f"fc{n_layer+1}", 
                                    nn.Linear(last_num, last_num//2)))
                    last_num = last_num//2
                network.append((f"rfc{n_layer+1}",
                                   nn.ReLU()))
        network.append(("final", nn.Linear(128, n_actions)))
        self.network = nn.Sequential(OrderedDict(network))

        print("--- Network Initialized as : ---")
        print(self.network)
        print("-------")

        self.observation_keys = state_keys
        self.action_keys = action_keys

    def forward(self, x):
        if not isinstance(x, dict):
            x = self.network(x)
        else:
            with torch.no_grad():
                x = pyc_to_torch(x, indices=self.observation_keys)
                x = self.forward(x)
                x = torch_to_pyc(x, indices=self.action_keys)
        return x