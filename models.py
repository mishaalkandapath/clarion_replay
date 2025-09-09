from collections import OrderedDict
from typing import Union, List

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

class myModule(nn.Module):
    def device(self):
        return next(self.parameters()).device

class DQN(myModule):
    def __init__(self, state_keys, action_keys, n_layers=8, a2c=False):
        super().__init__()

        n_observations = len(state_keys) + (2 if a2c else 0)
        n_actions = len(action_keys) + int(a2c)
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
    
class GRULayer(myModule):
    """Custom GRU layer built from scratch using PyTorch primitives"""
    
    def __init__(self, input_size, hidden_size, bias=True):
        super(GRULayer, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
    
        self.input_to_reset = nn.Linear(input_size, hidden_size, bias=False)
        self.hidden_to_reset = nn.Linear(hidden_size, hidden_size, bias=bias)
        
        self.input_to_update = nn.Linear(input_size, hidden_size, bias=False)
        self.hidden_to_update = nn.Linear(hidden_size, hidden_size, bias=bias)
        
        self.input_to_new = nn.Linear(input_size, hidden_size, bias=False)
        self.hidden_to_new = nn.Linear(hidden_size, hidden_size, bias=bias)
        
    def forward(self, x, h_0=None, record_gates=False):
        """
        Forward pass through GRU layer
        Args:
            x: Input tensor of shape (batch_size, seq_len, input_size)
            h_0: Initial hidden state of shape (batch_size, hidden_size)
        Returns:
            outputs: All hidden states of shape (batch_size, seq_len, hidden_size)
            h_n: Final hidden state of shape (batch_size, hidden_size)
        """
        batch_size, seq_len, _ = x.size()
        
        if h_0 is None:
            h_0 = torch.zeros(batch_size, self.hidden_size, device=x.device, dtype=x.dtype)
        
        outputs = []
        h_t = h_0

        r_record, z_record, h_new_record, h_record = [], [], [], []
        
        for t in range(seq_len):
            if record_gates:
                h_record.append(h_t.detach().cpu())

            x_t = x[:, t, :]  # Current input: (batch_size, input_size)
            
            r_t = torch.sigmoid(
                self.input_to_reset(x_t) + self.hidden_to_reset(h_t)
            )
            
            z_t = torch.sigmoid(
                self.input_to_update(x_t) + self.hidden_to_update(h_t)
            )
            
            n_t = torch.tanh(
                self.input_to_new(x_t) + self.hidden_to_new(r_t * h_t)
            )
            
            h_t = (1 - z_t) * h_t + z_t * n_t
            
            outputs.append(h_t.unsqueeze(1))  # Add time dimension back

            if record_gates:
                r_record.append(r_t.detach().cpu())
                z_record.append(z_t.detach().cpu())
                h_new_record.append(n_t.detach().cpu())
        
        outputs = torch.cat(outputs, dim=1)  # (batch_size, seq_len, hidden_size)
        if record_gates: return outputs, h_t, torch.stack(r_record, dim=1), torch.stack(z_record, dim=1), torch.stack(h_new_record, dim=1), torch.stack(h_record, dim=1)
        return outputs, h_t


class RNN(myModule):
    """Base RNN class that can use either vanilla RNN cells or GRU cells"""
    
    def __init__(self, input_size, hidden_size, 
                 out_size=0, out_act=nn.ReLU, num_layers=1, 
                 use_gru=False, hidden_bias=True, out_bias=True, learn_init=False):
        super(RNN, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.out_size = out_size
        self.num_layers = num_layers
        self.use_gru = use_gru
        self.learn_init = learn_init
        
        self.layers = nn.ModuleList()
        
        last_num = hidden_size
        self.layers.append(GRULayer(input_size, hidden_size, hidden_bias))
        init_states = [nn.Parameter(torch.zeros(hidden_size))]
        for n_layer in range(num_layers):
            if n_layer < num_layers//2:
                latest_layer = GRULayer(last_num, 
                                            last_num*2)
                init_states.append(nn.Parameter(torch.zeros(last_num * 2)))
                last_num = last_num * 2
            else:
                latest_layer = GRULayer(last_num, 
                                          last_num//2)
                init_states.append(nn.Parameter(torch.zeros(last_num//2)))
                last_num = last_num//2
            self.layers.append(latest_layer)
                
        if out_size: 
            self.layers.append(nn.Linear(hidden_size, out_size, bias=out_bias))
            self.out_act = out_act

        if self.learn_init:
            self.initial_states = nn.ParameterList([
                init_states[i]
                for i in range(num_layers+1)
            ])
        print(self.layers)
    
    def forward(self, x, h_0=None):
        """
        Forward pass through multi-layer RNN
        Args:
            x: Input tensor of shape (batch_size, seq_len, input_size)
            h_0: Initial hidden states for all layers, list of tensors or None
        Returns:
            outputs: All hidden states from final layer (batch_size, seq_len, hidden_size)
            final_hiddens: Final hidden states from all layers, list of tensors
        """
        batch_size = x.size(0)
        
        if h_0 is None and self.learn_init:
            h_0 = [
                state.unsqueeze(0).expand(batch_size, -1)
                for state in self.initial_states
            ]
        elif h_0 is None:
            h_0 = [None] * self.num_layers
        elif not isinstance(h_0, list):
            # h_0 = [h_0] + [None] * (self.num_layers - 1)
            raise Exception
        elif len(h_0) < self.num_layers:
            # h_0 = h_0 + [None] * (self.num_layers - len(h_0))
            raise Exception
        outputs = x
        final_hiddens = [] # per layer --for last timestep
        
        for i in range(len(self.layers) - (self.out_size != 0)):
            layer = self.layers[i]
            # outputs - the output of the hidden layer -- the h_t forall t
            outputs, h_n = layer(outputs, h_0[i])
            final_hiddens.append(h_n)
        if self.out_size:
            outputs = self.out_act(self.layers[-1](outputs))
        return outputs, final_hiddens
