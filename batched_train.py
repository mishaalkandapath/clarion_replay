import pickle
import signal
import sys
import os
from itertools import product
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tqdm import tqdm 

import waitGPU
waitGPU.wait(memory_ratio=0.001,
             gpu_ids=[0,1], interval=10, nproc=1, ngpu=1)

import torch 
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader

from q_learning import pyc_to_torch, torch_to_pyc, DQN, ReplayMemory, Transition
from batched_data_prep import STATE_KEYS, ACTION_KEYS  

STATE_KEYS = list(product(STATE_KEYS, 
                      ["1", "2", "3", "4", "5", "6"]))
interrupted = False
train_obj_global = None
run_name_global = None

def signal_handler(signum, frame):
    global interrupted, train_obj_global, run_name_global
    print("\n\nReceived interrupt signal (Ctrl+C). Saving model and exiting gracefully...")
    interrupted = True
    
    if train_obj_global is not None and run_name_global is not None:
        try:
            os.makedirs(f"data/run_data/{run_name_global}", exist_ok=True)
            save_path = f"data/run_data/{run_name_global}/interrupted_model.pt"
            torch.save(train_obj_global.policy_net.state_dict(), save_path)
            print(f"Model saved to: {save_path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    print("Exiting...")
    sys.exit(0)

class QValPlotter:
    def __init__(self, output_dir='plots', figsize=(10, 6)):
        self.output_dir = output_dir
        self.figsize = figsize
        
        # Store all data
        self.A = []
        self.B = []
        
        # Track what's been plotted to avoid replotting
        self.last_plotted_length = 0
        
        # Reusable figure and axis
        self.fig = None
        self.ax = None
        
    def update_and_save(self, new_A, new_B, filename="qvals_train.png"):
        """Update data and save plot, only plotting new segments"""
        
        if len(new_A) == 0:
            return
            
        assert len(new_A) == len(new_B), "A and B must have same length"
        
        # Add new data
        self.A.extend(new_A)
        self.B.extend(new_B)
        
        # Create or reuse figure
        if self.fig is None:
            self.fig, self.ax = plt.subplots(figsize=self.figsize)
            self._setup_plot()
        
        # Only plot new segments and points
        self._plot_new_data()
        
        # Update last plotted length
        self.last_plotted_length = len(self.A)
        
        # Save
        filepath = os.path.join(self.output_dir, filename)
        self.fig.savefig(filepath, dpi=300, bbox_inches='tight')
        
    def _setup_plot(self):
        """Setup plot labels and legend (only called once)"""
        self.ax.set_xlabel('Steps (in no particular order)')
        self.ax.set_ylabel('Q-Values')
        self.ax.set_title("Qvals over training")
        
        # Add legend
        red_patch = mpatches.Patch(color='red', label='B ≠ 1')
        green_patch = mpatches.Patch(color='green', label='B = 1')
        self.ax.legend(handles=[red_patch, green_patch], loc="upper right")
        
    def _plot_new_data(self):
        """Plot only the new data points and segments"""
        start_idx = self.last_plotted_length
        end_idx = len(self.A)
        
        if start_idx >= end_idx:
            return
            
        # Plot new segments
        for i in range(start_idx, end_idx):
            if i == 0:
                continue
                
            color = 'green' if self.B[i] == 1 else 'red'
            
            # Only plot segment if previous point exists and was plotted
            if i > 0:
                self.ax.plot([i-1, i], [self.A[i-1], self.A[i]], color=color, linewidth=2)
        
        # # Plot new points
        # for i in range(start_idx, end_idx):
        #     color = 'green' if self.B[i] == 1 else 'red'
        #     self.ax.plot(i, self.A[i], 'o', color=color, markersize=1)
        
        # Update axis limits efficiently
        if end_idx > 0:
            self.ax.set_xlim(-0.5, end_idx - 0.5)
            y_min, y_max = min(self.A), max(self.A)
            y_range = y_max - y_min
            self.ax.set_ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
    
    def close(self):
        """Close the figure"""
        if self.fig is not None:
            plt.close(self.fig)
            self.fig = None
            self.ax = None

class EpisodeDataset(Dataset):
    def __init__(self, dataset_files: List[str]):
        data = []
        for file in dataset_files:
            with open(file, "rb") as f:
                data += pickle.load(f)
        self.data = data
        self.state_right_actions = {}
        self.states_ref = []
        self.state_to_right_actions()
        print("--- Finished Dataset Initialization ---")
        print(f"{len(self.states_ref)} Unique States")
    
    def state_to_right_actions(self):
        # a dictionary from state to the right actions
        for entry in tqdm(self.data):
            state, action, reward, next_state = entry
            if reward != -1:
                if all(torch.any(s != state) for s in self.states_ref):
                    index = len(self.states_ref)
                    self.states_ref.append(state)
                else:
                    index = [i for i, s in enumerate(self.states_ref) if torch.all(s == state)][0]
                if index not in self.state_right_actions:
                    self.state_right_actions[index] = []
                self.state_right_actions[index].append(action)

    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index: int) -> Transition:
        state, action, reward, next_state = self.data[index]
        reward = reward if reward != -0.1 else 0.5
        return Transition(
            state, torch.tensor([action]), next_state, torch.tensor([reward], dtype=torch.float32)
        )

class TrainBatched:
    def __init__(self, model_path: str= None,
                 gamma: float = 0.9, tau: float=0.005, lr :float=1e-3,
                 device="cpu"):
        
        policy_net = DQN(STATE_KEYS, ACTION_KEYS)
        if model_path:
            policy_net.load_state_dict(torch.load(model_path, weights_only=True))
        
        self.policy_net = policy_net.to(device)
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
                    self.policy_net(non_final_next_states).max(1).values
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

        return loss.item(), state_action_values

def transitions_collate(batch: List[Transition]) -> Tuple[torch.tensor]:
    batch = Transition(*zip(*batch))
    non_final_mask = torch.tensor(
        tuple(map(lambda s: s is not None, batch.next_state)),
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

def check_accuracy(policy_net: DQN, 
                   dataset: EpisodeDataset,
                   device: str) -> float:
    batch_size = min(8192, len(dataset.states_ref))
    with torch.no_grad():
        states = dataset.states_ref.copy()
        offset_count = 0
        actions = []
        correct = 0
        while states:
            states_batch = states[:batch_size]
            states_batch = torch.stack(states_batch).to(device)
            action_vals = policy_net(states_batch).argmax(dim=-1)
            states_batch = states_batch.to(torch.device("cpu"))
            for i in range(states_batch.size(0)):
                action = action_vals[i].detach().item()
                index = [j for j, s in enumerate(dataset.states_ref) if torch.all(states_batch[i] == s)][0]
                correct += (action in dataset.state_right_actions[index])
            actions.extend(action_vals.detach().tolist())
            states = states[batch_size:]
            offset_count += batch_size
    return correct/len(dataset.states_ref), actions


def training(train_obj: TrainBatched, dataset_files: List[str], 
             run_name: str,
             epochs=100, batch_size=128,
             device="cpu",
             run_until_accurate=False):
    global interrupted
    dataset = EpisodeDataset(dataset_files)
    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=5, collate_fn=transitions_collate)
    losses = []
    accuracies = [0]
    epochs_left = epochs
    running_count = 0
    action_buffer = []

    while (accuracies[-1] < 0.999 and run_until_accurate) or epochs_left:
        if interrupted:
            print("Training interrupted by user. Exiting...")
            break
        qval_plotter = QValPlotter(f"data/run_data/{run_name}/figures/")
        pbar = tqdm(range(epochs))
        epochs_left = epochs

        for _ in pbar:
            if interrupted:
                print("\nTraining interrupted by user. Exiting...")
                qval_plotter.close()
                return
            
            qvals = []
            rewards = []
            for batch in dataloader:
                if interrupted:
                    print("\nTraining interrupted by user. Exiting...")
                    qval_plotter.close()
                    return
        
                batch = [t.to(device=device) for t in batch]
                _, _, reward, _, _ = batch
                loss, qval = train_obj.optimize_model(batch)
                losses += [loss]
                fig = plt.figure()
                plt.plot(losses)
                plt.savefig(f"data/run_data/{run_name}/figures/losses.png")
                plt.close(fig)
                qvals.extend(qval.squeeze(1).detach().tolist())
                rewards.extend((reward > 0).squeeze(1).detach().tolist())
                pbar.set_description(f"Loss: {loss}")

            qval_plotter.update_and_save(qvals, rewards, filename=f"qvals_train_{running_count}.png")
            epochs_left -= 1 

        accuracy, action_vals = check_accuracy(train_obj.policy_net, dataset, device)
        action_buffer.extend(action_vals)
        accuracies.append(accuracy)
        fig = plt.figure()
        plt.plot(accuracies)
        plt.savefig(f"data/run_data/{run_name}/figures/accuracies.png")
        plt.close(fig)
        fig = plt.figure()
        plt.plot(action_buffer)
        plt.savefig(f"data/run_data/{run_name}/figures/actions.png")
        plt.close(fig)
        qval_plotter.close()
        running_count +=1

def testing(model_path: str, dataset_files: List[str], test_name:str,
            device="cpu"):
    policy_net = DQN(STATE_KEYS, ACTION_KEYS)
    policy_net.load_state_dict(torch.load(model_path, weights_only=True))
    policy_net = policy_net.to(device)
    dataset = EpisodeDataset(dataset_files)

    action_buffer = []
    accuracy, action_vals = check_accuracy(policy_net, dataset, device)
    action_buffer.extend(action_vals)
    fig = plt.figure()
    plt.plot(action_buffer)
    plt.savefig(f"data/run_data/{test_name}/figures/actions.png")
    plt.close(fig)

    print(f"--- Test ended with accuracy {accuracy}----")

if __name__ == "__main__":
    import argparse
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--epochs", type=int, default = 10)
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--gamma", type=float, default=0.9)
    parser.add_argument("--tau", type=float, default=0.005)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--dataset_files", nargs="+", required=True)
    parser.add_argument("--run_name", required=True)
    parser.add_argument("--cpu", action="store_true")
    parser.add_argument("--model", default=None)
    parser.add_argument("--run_until_accurate", action="store_true")

    args = parser.parse_args()
    torch.manual_seed(0)

    os.makedirs(f"data/run_data/{args.run_name}/figures", exist_ok=True)

    
    if not args.test:
        train_obj = TrainBatched(args.model,
                                args.gamma, args.tau, args.lr,
                                device=torch.device("cuda" if not args.cpu or not torch.cuda.is_available() else "cpu"))
        training(train_obj, args.dataset_files, 
                args.run_name,
                args.epochs, args.batch_size,
                device=torch.device("cuda" if not args.cpu or not torch.cuda.is_available() else "cpu"),
                run_until_accurate=args.run_until_accurate)
        
        torch.save(train_obj.policy_net.state_dict(), f"data/run_data/{args.run_name}/goal_net.pt")

        #dump hyperparameters
        f = open(f"data/run_data/{args.run_name}/hyperparams.pkl", "wb")
        pickle.dump([args.epochs, args.batch_size, args.gamma, args.tau, args.lr], f)
        f.close()
    else:
        testing(args.model, args.dataset_files, args.run_name, 
                device=torch.device("cuda" if not args.cpu or not torch.cuda.is_available() else "cpu"))