from collections import defaultdict, deque
from typing import List, Tuple, Optional
import json
from itertools import product
import random
import math
import sys
import signal

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from tqdm import tqdm

from models import RNN, DQN
from batched_rl_env import BatchedBrickEnvironment
from scaffolded_training import get_grids_by_number, TEST_GRIDS
from batched_data_prep import STATE_KEYS, ACTION_KEYS

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
            torch.save(train_obj_global.model.state_dict(), save_path)
            if train_obj_global.algorithm == "q_learning":
                torch.save(train_obj_global.target_model.state_dict(), save_path.replace("model", "target_model"))
            print(f"Model saved to: {save_path}")
        except Exception as e:
            print(f"Error saving model: {e}")
    
    print("Exiting...")
    sys.exit(0)

class RLEnvTrainer:
    """
    Unified trainer class implementing both advantage actor-critic and Q-learning algorithms
    for batched brick environment. Handles variable-length episodes with proper masking.
    """
    
    def __init__(self, model, env, algorithm='a2c', 
                 lr=7e-4, lr_init=0, gamma=0.9, 
                 beta_entropy=0.005, beta_critic=0.05, 
                 # Q-learning specific parameters
                 epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995,
                 tau=100, buffer_size=10000, min_buffer_size=1000,
                 n_layers=4, logger=None, device=None):
        """
        Args:
            model: RNN model that outputs both policy logits and value estimates (A2C) or Q-values (Q-learning)
            env: BatchedBrickEnvironment instance
            algorithm: 'a2c' or 'q_learning'
            lr: Learning rate for actor (policy) parameters
            lr_init: Learning rate for initial states
            gamma: Discount factor
            beta_entropy: Entropy regularization coefficient (A2C only)
            beta_critic: Critic loss coefficient (A2C only)
            epsilon_start: Starting epsilon for epsilon-greedy exploration (Q-learning only)
            epsilon_end: Final epsilon value (Q-learning only)
            epsilon_decay: Epsilon decay rate (Q-learning only)
            target_update_freq: How often to update target network (Q-learning only)
            buffer_size: Replay buffer size (Q-learning only)
            min_buffer_size: Minimum buffer size before training (Q-learning only)
            logger: Optional logger
            device: Device to run on
        """

        self.model = model
        self.env = env
        self.algorithm = algorithm
        self.gamma = gamma
        self.logger = logger

        # A2C specific parameters
        self.beta_entropy = beta_entropy
        self.beta_critic = beta_critic
        
        # Q-learning specific parameters
        self.epsilon_start = epsilon_start
        self.epsilon= self.epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.tau = tau
        self.min_buffer_size = min_buffer_size
        self.training_step = 0
        
        # Initialize replay buffer for Q-learning
        if algorithm == 'q_learning':
            self.replay_buffer = deque(maxlen=buffer_size)
            # Create target network for Q-learning
            if type(model) is DQN:
                self.target_model = DQN(STATE_KEYS, ACTION_KEYS, n_layers, a2c=False)
            else:
                self.target_model = RNN(model.input_size, model.hidden_size, model.output_size,
                                      out_act=model.out_act, num_layers=model.num_layers, 
                                      use_gru=model.use_gru, learn_init=model.learn_init)
            self.target_model.load_state_dict(model.state_dict())
            self.target_model.eval()
    
        # Setup optimizer
        if type(model) is not DQN and model.learn_init:
            self.optimizer = torch.optim.Adam([
                {'params': [p for name, p in model.named_parameters() 
                            if 'initial_states' not in name], 
                'lr': lr},
                
                {'params': model.initial_states.parameters(), 
                'lr': lr_init} 
            ], lr=lr)
        else:
            self.optimizer = optim.Adam(model.parameters(), lr=lr)

        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))

        self.model.to(self.device)
        if algorithm == 'q_learning':
            self.target_model.to(self.device)
        
    def get_model_outputs_batched(self, input_tensor, 
                                  hidden_state, target_network=False):
        """
        Get policy logits and value estimate from model for batched input.
        Assumes model outputs (batch, seq, features) where features == num_actions + 1 (A2C) or num_actions (Q-learning).
        """
        model_to_use = self.target_model if target_network and self.algorithm == 'q_learning' else self.model
        
        if type(model_to_use) is DQN:
            outputs = model_to_use(input_tensor)
            new_hidden = None
        else:
            outputs, new_hidden = model_to_use(input_tensor, hidden_state)
        
        # Assuming single step output: (batch, 1, features)
        if self.algorithm == 'a2c':
            policy_logits = outputs[:, 0, :-1]  # (batch, num_actions)
            value_estimate = outputs[:, 0, -1]   # (batch,)
            return policy_logits, value_estimate, new_hidden
        else:  # q_learning
            q_values = outputs[:, 0, :]  # (batch, num_actions)
            return q_values, new_hidden
    
    def select_action_batched(self, policy_logits_or_q_values, inference=False):
        """
        Select actions for entire batch based on policy logits (A2C) or Q-values (Q-learning).
        
        Args:
            policy_logits_or_q_values: (batch, num_actions) tensor
            inference: If True, use greedy selection; if False, sample (A2C) or use epsilon-greedy (Q-learning)
        """
        if self.algorithm == 'a2c':
            if not inference:
                action_probs = F.softmax(policy_logits_or_q_values, dim=-1)
                return torch.multinomial(action_probs, 1).squeeze(-1)  # (batch,)
            else:
                return policy_logits_or_q_values.argmax(-1)  # (batch,)
        else:  # q_learning
            sample = random.random()
            self.epsilon = self.epsilon_end + (self.epsilon_start - self.epsilon_end) * math.exp(-1. * self.training_step / self.epsilon_decay)
            if not inference and sample < self.epsilon:
                # Epsilon-greedy exploration
                batch_size = policy_logits_or_q_values.shape[0]
                return torch.randint(0, policy_logits_or_q_values.shape[-1], 
                                   (batch_size,), device=self.device)
            else:
                return policy_logits_or_q_values.argmax(-1)  # (batch,)
    
    def add_to_replay_buffer(self, states_seq, actions_seq, rewards_seq,
                              next_states_seq, dones_seq, mask):
        """
        Add episode data to replay buffer for Q-learning.
        """
        batch_size, seq_len = mask.shape
        
        for b in range(batch_size):
            valid_steps = mask[b].sum().item()
            for t in range(valid_steps):
                state = states_seq[t][b].cpu().numpy()
                action = actions_seq[t][b].item()
                reward = rewards_seq[t][b].item()
                
                if t + 1 < valid_steps:
                    next_state = states_seq[t + 1][b].cpu().numpy()
                    done = False
                else:
                    continue
                
                self.replay_buffer.append((state, action, reward, next_state, done))
    
    def sample_from_replay_buffer(self, batch_size=32):
        """
        Sample a batch of transitions from replay buffer.
        """
        batch = random.sample(self.replay_buffer, batch_size)
        
        states = torch.FloatTensor([t[0] for t in batch]).to(self.device)
        actions = torch.LongTensor([t[1] for t in batch]).to(self.device)
        rewards = torch.FloatTensor([t[2] for t in batch]).to(self.device)
        next_states = torch.FloatTensor([t[3] for t in batch]).to(self.device)
        dones = torch.BoolTensor([t[4] for t in batch]).to(self.device)
        
        return states, actions, rewards, next_states, dones
    
    def compute_q_learning_loss(self, batch_size=32):
        """
        Compute Q-learning loss using replay buffer.
        """
        if len(self.replay_buffer) < self.min_buffer_size:
            return torch.tensor(0.0, device=self.device)
        
        states, actions, rewards, next_states, dones = self.sample_from_replay_buffer(batch_size)
        
        states_input = states.unsqueeze(1)
        next_states_input = next_states.unsqueeze(1)
        
        # Get current Q-values
        current_q_values, _ = self.get_model_outputs_batched(states_input, None)
        current_q_values = current_q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Get next Q-values from target network
        with torch.no_grad():
            next_q_values, _ = self.get_model_outputs_batched(next_states_input, None, target_network=True)
            next_q_values = next_q_values.max(1)[0]
            target_q_values = rewards + (self.gamma * next_q_values * ~dones)
        
        loss = nn.SmoothL1Loss()(target_q_values, current_q_values)
        return loss
    
    def compute_returns_masked(self, rewards, dones_mask):
        """
        Compute discounted returns for variable-length episodes with masking.
        
        Args:
            rewards: (batch, max_seq_len) tensor of rewards
            values: (batch, max_seq_len) tensor of value estimates  
            dones_mask: (batch, max_seq_len) tensor indicating valid steps
        """
        batch_size, seq_len = rewards.shape
        returns = torch.zeros_like(rewards)
        
        # For each batch item, work backwards from its actual end
        for b in range(batch_size):
            # Find the last valid step for this batch item
            valid_steps = dones_mask[b].sum().item()
            if valid_steps == 0:
                continue
                
            R = 0.0  # No bootstrap for terminal states
            
            # Work backwards through valid steps only
            for t in reversed(range(valid_steps)):
                R = rewards[b, t] + self.gamma * R
                returns[b, t] = R
                
        return returns
    
    def compute_advantage_loss_batched(self, policy_logits_seq, actions_seq, 
                                     returns, values, mask):
        """
        Compute batched actor-critic loss components with masking.
        
        Args:
            policy_logits_seq: List of (batch, num_actions) tensors, one per timestep
            actions_seq: List of (batch,) tensors, one per timestep
            returns: (batch, seq_len) tensor of returns
            values: (batch, seq_len) tensor of value estimates
            mask: (batch, seq_len) tensor indicating valid steps
        """
        seq_len = len(policy_logits_seq)
        batch_size = policy_logits_seq[0].shape[0]
        
        # Compute advantages
        advantages = returns - values  # (batch, seq_len)
        advantages = torch.clamp(advantages, -5.0, 5.0)
        
        # Collect log probs and entropies for all valid steps
        log_probs = torch.zeros(batch_size, seq_len, device=self.device)
        entropies = torch.zeros(batch_size, seq_len, device=self.device)
        
        for t in range(seq_len):
            logits = policy_logits_seq[t]  # (batch, num_actions)
            actions = actions_seq[t]       # (batch,)
            dist = torch.distributions.Categorical(logits=logits)
            log_probs[:, t] = dist.log_prob(actions)
            entropies[:, t] = dist.entropy()
        
        # Apply mask to only include valid steps
        masked_log_probs = log_probs * mask
        masked_entropies = entropies * mask  
        masked_advantages = advantages * mask
        
        valid_steps = mask.sum()
        if valid_steps > 0:
            actor_loss = -(masked_log_probs * masked_advantages.detach()).sum() / valid_steps
            entropy_bonus = masked_entropies.sum() / valid_steps
            actor_loss = actor_loss - self.beta_entropy * entropy_bonus
            
            # Critic loss: only on valid steps
            masked_returns = returns * mask
            masked_values = values * mask
            critic_loss = 0.5 * F.mse_loss(masked_returns, masked_values, reduction='sum') / valid_steps
        else:
            actor_loss = torch.tensor(0.0, device=self.device)
            critic_loss = torch.tensor(0.0, device=self.device)
            
        return actor_loss, critic_loss, advantages.detach()
    
    def run_episode_batch(self, inference=False):
        """
        Run a full batch of episodes to completion.
        
        Returns:
            episode_data: Dictionary containing all episode information
        """
        batch_size = self.env.batch_size
        
        # Initialize episode storage
        states_seq = []      # List of (batch, state_dim) tensors
        actions_seq = []     # List of (batch,) tensors  
        rewards_seq = []     # List of (batch,) tensors
        policy_logits_seq = [] # List of (batch, num_actions) tensors
        values_seq = []      # List of (batch,) tensors (A2C only)
        
        hidden_state = None
        states = self.env.get_current_states().to(self.device)  # (batch, state_dim)
        
        # Track which episodes are still running
        max_possible_steps = max(self.env.max_lens)
        best_lens = np.array(self.env.max_lens)//4
        active_episodes = torch.ones(batch_size, dtype=torch.bool, device=self.device)
        mask = torch.ones(batch_size, max_possible_steps, 
                          dtype=torch.bool, device=self.device)
        
        step_count = 0
        while active_episodes.any() and step_count < max_possible_steps:
            if not states_seq and self.algorithm != "q_learning":
                model_input = torch.concat([states, torch.zeros(batch_size, 2).to(states.device)], dim=-1)
            elif self.algorithm != "q_learning":
                model_input = torch.concat([states, 
                                            rewards_seq[-1].unsqueeze(-1), actions_seq[-1].unsqueeze(-1)], dim=-1)
            else:
                model_input = states

            model_input = model_input.unsqueeze(1) # (batch, 1, state_dim+2) for RNN
            
            if self.algorithm == 'a2c':
                policy_logits, values, new_hidden = self.get_model_outputs_batched(
                    model_input, hidden_state)
                values_seq.append(values.to(self.device))
            else:  # q_learning
                policy_logits, new_hidden = self.get_model_outputs_batched(
                    model_input, hidden_state)
            
            actions = self.select_action_batched(policy_logits, 
                                                 inference=inference)
            new_states, rewards, dones = self.env.step(actions)
        
            dones = dones.to(self.device)
            states_seq.append(states.to(self.device))
            actions_seq.append(actions.to(self.device))  
            rewards_seq.append(rewards.to(self.device))
            policy_logits_seq.append(policy_logits)
            
            states = new_states.to(self.device)
            hidden_state = new_hidden
            
            # Update active episodes
            mask[:, step_count] = active_episodes.clone()
            active_episodes = active_episodes & (~dones)
            step_count += 1
        
        seq_len = len(states_seq)
        mask = mask[:, :seq_len]
        
        # Stack sequences
        rewards_tensor = torch.stack(rewards_seq, dim=1)  # (batch, seq_len)
        
        episode_data = {
            'states_seq': states_seq,
            'actions_seq': actions_seq,
            'rewards_seq': rewards_seq, 
            'policy_logits_seq': policy_logits_seq,
            'mask': mask,
            'episode_lengths': mask.sum(dim=1)/torch.from_numpy(best_lens).to(mask.device),
            'best_lengths': best_lens,
            'total_rewards': (rewards_tensor * mask).sum(dim=1)
        }
        
        if self.algorithm == 'a2c':
            values_tensor = torch.stack(values_seq, dim=1)    # (batch, seq_len)
            returns = self.compute_returns_masked(rewards_tensor, mask)
            episode_data.update({
                'values_tensor': values_tensor,
                'returns': returns
            })
        
        return episode_data
    
    def train_step(self):
        """
        Run one training step: episode batch to completion + backpropagation.
        """
        self.model.train()
        episode_data = self.run_episode_batch(inference=False)
        
        if self.algorithm == 'a2c':
            actor_loss, critic_loss, advantages = self.compute_advantage_loss_batched(
                episode_data['policy_logits_seq'],
                episode_data['actions_seq'], 
                episode_data['returns'],
                episode_data['values_tensor'],
                episode_data['mask']
            )
            total_loss = actor_loss + self.beta_critic * critic_loss
            
            self.optimizer.zero_grad()
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            self.optimizer.step()
            
            stats = {
                'actor_loss': actor_loss.item(),
                'critic_loss': critic_loss.item(), 
                'total_loss': total_loss.item(),
                'train_mean_episode_length': episode_data['episode_lengths'].float().mean().item(),
                'train_mean_episode_reward': episode_data['total_rewards'].float().mean().item(),
                'advantage_mean': advantages.mean().item(),
                'advantage_std': advantages.std().item()
            }
            
        else:  # q_learning
            # Add episode data to replay buffer
            self.add_to_replay_buffer(
                episode_data['states_seq'],
                episode_data['actions_seq'],
                episode_data['rewards_seq'],
                episode_data['states_seq'][1:] + [episode_data['states_seq'][-1]],  # next_states
                [torch.zeros_like(episode_data['actions_seq'][0], dtype=torch.bool)] * (len(episode_data['actions_seq']) - 1) + [torch.ones_like(episode_data['actions_seq'][-1], dtype=torch.bool)],  # dones
                episode_data['mask']
            )
            
            # Train on replay buffer
            q_loss = self.compute_q_learning_loss()
            
            if q_loss.item() > 0:
                self.optimizer.zero_grad()
                q_loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                self.optimizer.step()
            
            # Update target network
            target_net_state_dict = self.target_model.state_dict()
            policy_net_state_dict = self.model.state_dict()
            for key in policy_net_state_dict:
                target_net_state_dict[key] = policy_net_state_dict[key]*self.tau + target_net_state_dict[key]*(1-self.tau)
            self.target_model.load_state_dict(target_net_state_dict)
            
            self.training_step += 1
            stats = {
                'q_loss': q_loss.item(),
                'total_loss': q_loss.item(),
                'epsilon': self.epsilon,
                'buffer_size': len(self.replay_buffer),
                'train_mean_episode_length': episode_data['episode_lengths'].float().mean().item(),
                'train_mean_episode_reward': episode_data['total_rewards'].float().mean().item(),
            }
        
        # Reinitialize environments for next batch
        self.env._initialize_all_environments()
        
        return stats
    
    def train(self, run_name):
        """
        Train for specified number of steps.
        """
        best_train_loss = float("inf")
        best_test_acc = -float("inf")
        best_test_grid_correctness =  -float("inf")
        best_mean_length = float("inf")
        step = 0
        pbar = tqdm(total=500)
        while (best_test_acc < 0.99 and best_test_grid_correctness < 0.99) or best_mean_length > 1.02:
            stats = self.train_step()
            if stats['total_loss'] < best_train_loss:
                best_train_loss = stats['total_loss']
                torch.save(self.model.state_dict(), f"data/run_data/{run_name}/best_train_goal_net.pt")
                if self.algorithm=="q_learning":
                    torch.save(self.model.state_dict(), f"data/run_data/{run_name}/best_target_train_goal_net.pt")

            if step % 500 == 0:
                eval_stats = self.evaluate()
                acc = eval_stats["accuracy"] 
                correctness = eval_stats["grid_correctness"]
                mean_length = eval_stats["mean_length"]
                if correctness > best_test_grid_correctness:
                    torch.save(self.model.state_dict(), f"data/run_data/{run_name}/best_test_goal_net.pt")
                    if self.algorithm=="q_learning":
                        torch.save(self.model.state_dict(), f"data/run_data/{run_name}/best_target_test_goal_net.pt")
                    best_test_acc = acc
                    best_test_grid_correctness = correctness
                    best_mean_length = mean_length
                stats = eval_stats | stats
                self.logger.log(stats)
                pbar = tqdm(total=500)
            step+=1
            pbar.update(1)
        
    
    def evaluate(self, num_episodes=128):
        """
        Evaluate model performance over multiple episodes.
        """
        self.model.eval()
        
        total_rewards = []
        episode_lengths = []
        correctness = 0
        correctness_denom = 0
        grid_correctness = 0
        with torch.no_grad():
            for _ in range(num_episodes // self.env.batch_size):
                episode_data = self.run_episode_batch(inference=True)
                total_rewards.extend(episode_data['total_rewards'].cpu().numpy())
                episode_lengths.extend(episode_data['episode_lengths'].cpu().numpy())
                rews = torch.stack(episode_data["rewards_seq"], dim=-1)
                mask = episode_data["mask"]
                correctness += torch.sum((rews != -1) & (rews != 0))
                correctness_denom += torch.sum(mask)

                if (t := torch.count_nonzero(rews == 1)):
                    grid_correctness += t
                # Reinitialize for next evaluation batch
                self.env._initialize_all_environments()
        
        return {
            'mean_reward': np.mean(total_rewards),
            'mean_length': np.mean(episode_lengths),
            'std_length': np.std(episode_lengths),
            'accuracy': correctness/correctness_denom,
            "grid_correctness": grid_correctness/128
        }

if __name__ == "__main__":
    import argparse
    import os
    import wandb
    import pickle

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser("A2C/Q-Learning trainer")

    # Algorithm selection
    algorithm_group = parser.add_mutually_exclusive_group(required=True)
    algorithm_group.add_argument("--a2c", action="store_true", help="Use Advantage Actor-Critic")
    algorithm_group.add_argument("--q_learning", action="store_true", help="Use Q-Learning")

    # Model architecture
    parser.add_argument("--mlp", action="store_true")
    parser.add_argument("--d_hidden", type=int, required=True, help="Hidden layer size")
    parser.add_argument("--n_layers", type=int, required=True, help="Number of RNN layers")
    parser.add_argument("--gru", action="store_true", help="Use GRU?")
    parser.add_argument("--learn_init", action="store_true")

    # Common parameters
    parser.add_argument("--run_name", type=str, required=True, help="Name of run")
    parser.add_argument("--ctd_from", type=str, default=None)
    parser.add_argument("--lr", type=float, default=7e-4)
    parser.add_argument("--lr_init", type=float, default=0)
    parser.add_argument("--gamma", type=float, default=0.97)
    parser.add_argument("--batch_size", type=int, required=True)
    
    # A2C specific parameters
    a2c_group = parser.add_argument_group('A2C parameters')
    a2c_group.add_argument("--beta_entropy", type=float, default=0.05)
    a2c_group.add_argument("--beta_critic", type=float, default=0.05)
    
    # Q-Learning specific parameters
    q_group = parser.add_argument_group('Q-Learning parameters')
    q_group.add_argument("--epsilon_start", type=float, default=0.9)
    q_group.add_argument("--epsilon_end", type=float, default=0.01)
    q_group.add_argument("--epsilon_decay", type=float, default=500)
    q_group.add_argument("--tau", type=float, default=0.005)
    q_group.add_argument("--buffer_size", type=int, default=10000)
    q_group.add_argument("--min_buffer_size", type=int, default=1000)
    
    args = parser.parse_args()
    torch.manual_seed(0)

    # Determine algorithm
    algorithm = 'a2c' if args.a2c else 'q_learning'

    # Setup wandb config
    config = {
            "learning_rate": args.lr,
            "learning_rate_init": args.lr_init,
            "batch_size": args.batch_size,
            "gamma": args.gamma,
            "num_layers": args.n_layers,
            "beta_entropy": args.beta_entropy,
            "beta_critic": args.beta_critic,
            "n_hidden": args.d_hidden if not args.mlp else 0
        }

    if algorithm == 'a2c':
        config.update({
            "beta_entropy": args.beta_entropy,
            "beta_critic": args.beta_critic,
        })
    else:
        config.update({
            "epsilon_start": args.epsilon_start,
            "epsilon_end": args.epsilon_end,
            "epsilon_decay": args.epsilon_decay,
            "tau": args.tau,
            "buffer_size": args.buffer_size,
            "min_buffer_size": args.min_buffer_size,
        })

    run = wandb.init(
        entity="mishaalkandapath",
        project="brickworld",
        config=config
    )

    os.makedirs(f"data/run_data/{args.run_name}/figures", exist_ok=True)
    g_n = get_grids_by_number(os.listdir("data/processed/train_data/train_stims/"), start_from=1)
    #unroll generator:
    data = []
    start_from = 1
    for grid_names in g_n:
        grid_names = [g for g in grid_names if g not in TEST_GRIDS[start_from]]
        data.append(grid_names)
        start_from+=1
    env = BatchedBrickEnvironment(data, args.batch_size)

    if args.mlp:
        model = DQN(STATE_KEYS, ACTION_KEYS, args.n_layers, a2c=(algorithm == 'a2c'))
    else:
        output_size = len(ACTION_KEYS) + 1 if algorithm == 'a2c' else len(ACTION_KEYS)
        model = RNN(len(STATE_KEYS)+2, args.d_hidden, output_size,
                    out_act=lambda x: x, num_layers=args.n_layers, use_gru=args.gru,
                    learn_init=args.learn_init)
    
    # Create trainer with appropriate parameters
    if algorithm == 'a2c':
        train_obj = RLEnvTrainer(
            model, env, algorithm=algorithm, lr=args.lr,
            lr_init=args.lr_init, gamma=args.gamma,
            beta_entropy=args.beta_entropy,
            beta_critic=args.beta_critic,
            logger=run,
            device=torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
    else:  # q_learning
        train_obj = RLEnvTrainer(
            model, env, algorithm=algorithm, lr=args.lr,
            lr_init=args.lr_init, gamma=args.gamma,
            epsilon_start=args.epsilon_start,
            epsilon_end=args.epsilon_end,
            epsilon_decay=args.epsilon_decay,
            tau=args.tau,
            buffer_size=args.buffer_size,
            min_buffer_size=args.min_buffer_size,
            n_layers=args.n_layers,
            logger=run,
            device=torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        )
    
    train_obj_global = train_obj
    run_name_global = args.run_name
    train_obj.train(run_name=args.run_name)
    with open(f"data/run_data/{args.run_name}/hyperparams.json", "w") as f:
        json.dump(config, f)