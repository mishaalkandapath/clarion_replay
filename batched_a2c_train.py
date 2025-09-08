from collections import defaultdict
from typing import List, Tuple, Optional
import json
from itertools import product

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from tqdm import tqdm

from models import RNN
from batched_rl_env import BatchedBrickEnvironment
from scaffolded_training import get_grids_by_number, TEST_GRIDS
from batched_data_prep import STATE_KEYS, ACTION_KEYS

class ActorCriticTrainer:
    """
    Trainer class implementing advantage actor-critic algorithm for batched brick environment.
    Handles variable-length episodes with proper masking.
    """
    
    def __init__(self, model, env, lr=7e-4, lr_init=0, gamma=0.9, 
                 beta_entropy=0.005, beta_critic=0.05, logger=None, device=None):
        """
        Args:
            model: RNN model that outputs both policy logits and value estimates
            env: BatchedBrickEnvironment instance
            lr: Learning rate for actor (policy) parameters
            lr_init: Learning rate for initial states
            gamma: Discount factor
            beta_entropy: Entropy regularization coefficient
            beta_critic: Critic loss coefficient
            logger: Optional logger
            device: Device to run on
        """
        self.model = model
        self.env = env
        self.gamma = gamma
        self.beta_entropy = beta_entropy
        self.beta_critic = beta_critic
    
        if model.learn_init:
            self.optimizer = torch.optim.Adam([
                {'params': [p for name, p in model.named_parameters() 
                            if 'initial_states' not in name], 
                'lr': lr},
                
                {'params': model.initial_states.parameters(), 
                'lr': lr_init} 
            ], lr=lr)
        else:
            self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.logger = logger

        self.device = device or (torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))

        self.model.to(self.device)
        
    def get_model_outputs_batched(self, input_tensor, hidden_state):
        """
        Get policy logits and value estimate from model for batched input.
        Assumes model outputs (batch, seq, features) where features == num_actions + 1.
        """
        outputs, new_hidden = self.model(input_tensor, hidden_state)
        
        # Assuming single step output: (batch, 1, features)
        policy_logits = outputs[:, 0, :-1]  # (batch, num_actions)
        value_estimate = outputs[:, 0, -1]   # (batch,)
        
        return policy_logits, value_estimate, new_hidden
    
    def select_action_batched(self, policy_logits, inference=False):
        """
        Select actions for entire batch based on policy logits.
        
        Args:
            policy_logits: (batch, num_actions) tensor of logits
            inference: If True, use greedy selection; if False, sample
        """
        if not inference:
            action_probs = F.softmax(policy_logits, dim=-1)
            return torch.multinomial(action_probs, 1).squeeze(-1)  # (batch,)
        else:
            return policy_logits.argmax(-1)  # (batch,)
    
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
        values_seq = []      # List of (batch,) tensors
        
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
            if not states_seq:
                model_input = torch.concat([states, torch.zeros(batch_size, 2).to(states.device)], dim=-1)
            else:
                model_input = torch.concat([states, 
                                            rewards_seq[-1].unsqueeze(-1), actions_seq[-1].unsqueeze(-1)], dim=-1)

            model_input = model_input.unsqueeze(1) # (batch, 1, state_dim+2) for RNN
            policy_logits, values, new_hidden = self.get_model_outputs_batched(
                model_input, hidden_state)
            
            actions = self.select_action_batched(policy_logits, 
                                                 inference=inference)
            new_states, rewards, dones = self.env.step(actions)
        
            dones = dones.to(self.device)
            states_seq.append(states.to(self.device))
            actions_seq.append(actions.to(self.device))  
            rewards_seq.append(rewards.to(self.device))
            policy_logits_seq.append(policy_logits)
            values_seq.append(values.to(self.device))
            
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
        values_tensor = torch.stack(values_seq, dim=1)    # (batch, seq_len)
        
        # Compute returns
        returns = self.compute_returns_masked(rewards_tensor, mask)
        
        return {
            'states_seq': states_seq,
            'actions_seq': actions_seq,
            'rewards_seq': rewards_seq, 
            'policy_logits_seq': policy_logits_seq,
            'values_tensor': values_tensor,
            'returns': returns,
            'mask': mask,
            'episode_lengths': mask.sum(dim=1)/torch.from_numpy(best_lens).to(mask.device),
            'best_lengths': best_lens,
            'total_rewards': (rewards_tensor * mask).sum(dim=1)
        }
    
    def train_step(self):
        """
        Run one training step: episode batch to completion + backpropagation.
        """
        self.model.train()
        episode_data = self.run_episode_batch(inference=False)
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
        
        # Reinitialize environments for next batch
        self.env._initialize_all_environments()
        
        return {
            'actor_loss': actor_loss.item(),
            'critic_loss': critic_loss.item(), 
            'total_loss': total_loss.item(),
            'train_mean_episode_length': episode_data['episode_lengths'].float().mean().item(),
            'train_mean_episode_reward': episode_data['total_rewards'].float().mean().item(),
            'advantage_mean': advantages.mean().item(),
            'advantage_std': advantages.std().item()
        }
    
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
        while (best_test_acc < 0.99 and best_test_acc < 0.99) or best_mean_length > 1.02:
            stats = self.train_step()
            if stats['actor_loss'] + stats['critic_loss'] < best_train_loss:
                best_train_loss = stats['actor_loss'] + stats['critic_loss']
                torch.save(self.model.state_dict(), f"data/run_data/{run_name}/best_train_goal_net.pt")

            if step % 500 == 0:
                eval_stats = self.evaluate()
                acc = eval_stats["accuracy"] 
                correctness = eval_stats["grid_correctness"]
                mean_length = eval_stats["mean_length"]
                if correctness > best_test_grid_correctness:
                    torch.save(self.model.state_dict(), f"data/run_data/{run_name}/best_test_goal_net.pt")
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

    parser = argparse.ArgumentParser("A2C trainer")

    parser.add_argument("--mlp", action="store_true")
    parser.add_argument("--d_hidden", type=int, required=True, help="Hidden layer size")
    parser.add_argument("--n_layers", type=int, required=True, help="Number of RNN layers")
    parser.add_argument("--run_name", type=str, required=True, help="Name of run")
    parser.add_argument("--ctd_from", type=str, default=None)
    parser.add_argument("--gru", action="store_true", help="Use GRU?")
    parser.add_argument("--lr", type=float, default=7e-4)
    parser.add_argument("--lr_init", type=float, default=0)
    parser.add_argument("--gamma", type=float, default=0.97)
    parser.add_argument("--beta_entropy", type=float, default=0.05)
    parser.add_argument("--beta_critic", type=float, default=0.05)
    parser.add_argument("--batch_size", type=int, required=True)
    parser.add_argument("--learn_init", action="store_true")
    
    args = parser.parse_args()
    torch.manual_seed(0)

    # if not args.test:
    run = wandb.init(
        entity="mishaalkandapath",
        project="brickworld",
        config={
            "learning_rate": args.lr,
            "learning_rate_init": args.lr_init,
            "batch_size": args.batch_size,
            "gamma": args.gamma,
            "num_layers": args.n_layers,
            "beta_entropy": args.beta_entropy,
            "beta_critic": args.beta_critic,
            "n_hidden": args.d_hidden if not args.mlp else 0
        }
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
    print([len(d) for d in data])
    env = BatchedBrickEnvironment(data, args.batch_size)
    model = RNN(len(STATE_KEYS)+2, args.d_hidden, len(ACTION_KEYS)+1,
                out_act=lambda x: x, num_layers=args.n_layers, use_gru=args.gru,
                learn_init=args.learn_init)
    train_obj = ActorCriticTrainer(model, env, lr=args.lr,
                                   lr_init=args.lr_init, gamma=args.gamma,
                                   beta_entropy=args.beta_entropy,
                                   beta_critic=args.beta_critic,
                                   logger=run,
                                   device=torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu"))
    
    train_obj.train(run_name=args.run_name)
    with open(f"data/run_data/{args.run_name}/hyperparams.json", "w") as f:
        json.dump({
                "learning_rate": args.lr,
                "learning_rate_init": args.lr_init,
                "batch_size": args.batch_size,
                "gamma": args.gamma,
                "num_layers": args.n_layers,
                "beta_entropy": args.beta_entropy,
                "beta_critic": args.beta_critic,
                "n_hidden": args.d_hidden if not args.mlp else 0
            }, f)