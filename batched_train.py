import pickle
from itertools import product
from typing import List, Tuple

import matplotlib.pyplot as plt
from tqdm import tqdm 
import torch 
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader

from q_learning import pyc_to_torch, torch_to_pyc, DQN, ReplayMemory, Transition
from batched_data_prep import STATE_KEYS, ACTION_KEYS  

STATE_KEYS = list(product(STATE_KEYS, 
                      ["1", "2", "3", "4", "5", "6"]))

def plot_qvals(A, B, output_dir='plots'):    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if len(A) == 0:
        plt.close(fig)
        return
        
    # Ensure B has the same length as A
    assert len(B) == len(A)
    
    # Create x-axis (indices)
    x = list(range(len(A)))
    
    # Plot segments with different colors
    for i in range(len(A)):
        if i == 0:
            continue
            
        color = 'green' if B[i] == 1 else 'red'
        ax.plot([x[i-1], x[i]], [A[i-1], A[i]], color=color, linewidth=2)
        
    # Plot points
    for i in range(len(A)):
        color = 'green' if B[i] == 1 else 'red'
        ax.plot(x[i], A[i], 'o', color=color, markersize=6)
    
    # Set labels and title
    ax.set_xlabel('Steps (in no particular order)')
    ax.set_ylabel('Q-Values')
    ax.set_title("Qvals over training")
    
    # Add legend
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color='red', label='B ≠ 1')
    green_patch = mpatches.Patch(color='green', label='B = 1')
    ax.legend(handles=[red_patch, green_patch])
    
    # Save and close
    filename = f"qvals_train.png"
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot saved: {filepath}")

class EpisodeDataset(Dataset):
    def __init__(self, dataset_files: List[str]):
        self.data += []
        for file in dataset_files:
            with open(file, "rb") as f:
                self.data += pickle.load(f)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index: int) -> Transition:
        state, action, next_state, reward = self.data[index]
        return Transition(
            state, torch.tensor([action]), next_state, torch.tensor([reward], dtype=torch.float32)
        )

class TrainBatched:
    def __init__(self,
                 gamma: float = 0.9, tau: float=0.005, lr :float=1e-3,
                 device="cpu"):
        
        policy_net = DQN(STATE_KEYS, ACTION_KEYS)
        target_net = DQN(STATE_KEYS, ACTION_KEYS)
        target_net.load_state_dict(policy_net.state_dict())
        
        self.policy_net = policy_net.to(device)
        self.target_net = target_net.to(device)
        self.optimizer = optim.Adam(policy_net.parameters(), lr=lr)

        #h-parameters
        self.tau = tau 
        self.gamma = gamma
        self.device = device

    def optimize_model(self, batch: List[torch.tensor]):
        state_batch, action_batch, reward_batch, non_final_next_states, non_final_mask = batch

        # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
        # columns of actions taken. These are the actions which would've been taken
        # for each batch state according to policy_net
        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # Compute V(s_{t+1}) for all next states.
        # Expected values of actions for non_final_next_states are computed based
        # on the "older" target_net; selecting their best reward with max(1).values
        # This is merged based on the mask, such that we'll have either the expected
        # state value or 0 in case the state was final.
        next_state_values = torch.zeros(state_batch.size(0), device=self.device)
        with torch.no_grad():
            if torch.any(non_final_mask):
                next_state_values[non_final_mask] = (
                    self.target_net(non_final_next_states).max(1).values
                )
        # Compute the expected Q values
        expected_state_action_values = (next_state_values * self.gamma).unsqueeze(
            1
        ) + reward_batch

        # Compute Huber loss
        criterion = nn.SmoothL1Loss()
        loss = criterion(state_action_values, expected_state_action_values)

        # Optimize the model
        self.optimizer.zero_grad()
        loss.backward()
        # In-place gradient clipping
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()
        self.soft_update()

        return loss.item(), state_action_values

    def soft_update(self):
        target_net_state_dict = self.target_net.state_dict()
        policy_net_state_dict = self.policy_net.state_dict()

        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[
                key
            ] * self.tau + target_net_state_dict[key] * (1.0 - self.tau)
        self.target_net.load_state_dict(target_net_state_dict)

def transitions_collate(batch: List[Transition], device="cpu") -> Tuple[torch.tensor]:
    batch = Transition(*zip(*batch))
    non_final_mask = torch.tensor(
        tuple(map(lambda s: s is not None, batch.next_state)),
        device=device,
        dtype=torch.bool,
    )
    non_final_next_states = torch.stack(
        [s for s in batch.next_state if s is not None]
    )
    state_batch = torch.stack(batch.state)
    action_batch = torch.stack(batch.action)
    reward_batch = torch.stack(batch.reward)
    return (state_batch, action_batch, 
            reward_batch, non_final_next_states, non_final_mask)

def training(train_obj: TrainBatched, dataset_files: List[str], 
             run_name: str,
             epochs=100, batch_size=128):
    dataset = EpisodeDataset(dataset_files)
    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=5, collate_fn=transitions_collate)
    losses = []
    qvals = []
    rewards = []
    for _ in tqdm(range(epochs)):
        for batch in dataloader:
            _, _, reward, _, _, _ = batch
            loss, qval = train_obj.optimize_model(batch)
            losses += [loss]
            qvals.extend(qval.squeeze(1).detach().tolist())
            rewards.extend((reward == 1).squeeze(1).detach().tolist())
            plt.plot(losses)
            plt.savefig(f"data/run_data/{run_name}/figures/losses.png")
            plot_qvals(qvals, rewards, f"data/run_data/{run_name}/figures/")


if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", default = 10)
    parser.add_argument("--batch_size", default=128)
    parser.add_argument("--gamma", default=0.9)
    parser.add_argument("--tau", default=0.005)
    parser.add_argument("--lr", default=1e-3)
    parser.add_argument("--dataset_files", nargs="+", required=True)
    parser.add_argument("--run_name", required=True)
    parser.add_argument("--cpu", action="store_true")

    args = parser.parse_args()
    torch.manual_seed(0)

    os.makedirs(f"data/run_data/{args.run_name}/figures", exist_ok=True)

    train_obj = TrainBatched(args.gamma, args.tau, args.lr,
                             device=torch.device("cuda" if not args.cpu or not torch.cuda.is_available() else "cpu"))
    training(train_obj, args.dataset_files, 
             args.run_name,
             args.epochs, args.batch_size)