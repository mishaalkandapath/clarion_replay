import numpy as np
import torch
from typing import List, Tuple
import random

from batched_data_prep import make_mlp_dict, action_is_right, make_grid_after_action, ACTION_KEYS
from utils import weighted_sample_without_replacement
class BatchedBrickEnvironment:
    def __init__(self, file_paths: List[List[str]], batch_size: int):
        self.file_paths = file_paths
        self.batch_size = batch_size
        
        self.target_grids = []
        for file_type in file_paths:
            self.target_grids.append([])
            for file_path in file_type:
                target_grid = np.load("data/processed/train_data/train_stims/"+file_path) 
                self.target_grids[-1].append(target_grid)
        
        # Initialize batch environments
        self.current_grids = []  # List of current grid states (numpy arrays)
        self.target_grids_batch = []  # List of target grids for current batch
        self.grid_tensors = []  # List of current states in tensor format
        self.step_counts = []  # Track steps for each environment
        self.dones = []
        self.max_lens = []  # Max length for each environment (4 * num_shapes)
        
        # Initialize all environments
        self._initialize_all_environments()
    
    def _initialize_all_environments(self):
        """Initialize all batch environments with random targets"""
        target_types = random.choices(range(4), k=self.batch_size)
        target_grids = []
        for i in range(4):
            sampler = weighted_sample_without_replacement if target_types.count(i) <= len(self.target_grids[i]) else random.choices
            target_grids.extend(sampler(self.target_grids[i],
                                            k=target_types.count(i)))
        for i in range(self.batch_size):
            self._initialize_single_environment(i, target_grids[i])
    
    def _initialize_single_environment(self, idx: int, target_grid: np.array):
        """Initialize a single environment at given index"""
        start_grid = np.zeros_like(target_grid, dtype=np.uint8)
        num_shapes = len(np.unique(target_grid)[np.unique(target_grid) != 0])
        max_len = 4 * num_shapes
        
        grid_tensor = torch.tensor(make_mlp_dict(target_grid), dtype=torch.float32) # current state - contains goal state
        
        if idx >= len(self.current_grids):
            # Append new environment
            self.current_grids.append(start_grid)
            self.target_grids_batch.append(target_grid)
            self.grid_tensors.append(grid_tensor)
            self.step_counts.append(0)
            self.dones.append(0)
            self.max_lens.append(max_len)
        else:
            # Replace existing environment
            self.current_grids[idx] = start_grid
            self.target_grids_batch[idx] = target_grid
            self.grid_tensors[idx] = grid_tensor
            self.step_counts[idx] = 0
            self.dones[idx] = 0
            self.max_lens[idx] = max_len
    
    def step(self, actions: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Take a step in all environments
        
        Args:
            actions: [batch_size] tensor of action indices
            
        Returns:
            states: [batch_size, state_dim] tensor of new states
            rewards: [batch_size] tensor of rewards
            dones: [batch_size] tensor of done flags
            infos: List of info dicts for each environment
        """
        states = []
        rewards = []
        dones = []
        
        for i in range(self.batch_size):
            if self.dones[i]:
                states.append(torch.zeros_like(self.grid_tensors[i]))
                rewards.append(0)
                dones.append(1)
                # Update grid tensor for next step
                self.grid_tensors[i] = torch.zeros_like(self.grid_tensors[i])
                continue

            action = actions[i].item()
            grid = self.current_grids[i]
            target_grid = self.target_grids_batch[i]
            
            # Check if action is right
            reward = -1
            done = False
            action_str = ACTION_KEYS[action]
            if action_is_right(target_grid, grid, action_str):
                # Calculate number of steps needed
                grid_shapes = (t := np.unique(grid))[t != 0].tolist()
                target_grid_shapes = (t := np.unique(target_grid))[t != 0].tolist()
                num_steps = len(target_grid_shapes) - len(grid_shapes)
                
                if num_steps == 1:
                    reward = 1
                    done = True
                    self.dones[i] = 1
                else:
                    reward = -0.1
                
                # Apply action and get new grid
                new_grid = make_grid_after_action(target_grid, grid, action_str)
                new_state = self.grid_tensors[i] + torch.tensor(make_mlp_dict(new_grid, target=True), dtype=torch.float32)
                new_state[new_state > 1] =1 # maintain goal inf, rem double counts
                
                # Update environment state
                self.current_grids[i] = new_grid
                
            else:
                # Wrong action, state doesn't change
                new_state = self.grid_tensors[i].clone()
            
            # Check if max length reached
            self.step_counts[i] += 1
            if self.step_counts[i] >= self.max_lens[i]:
                done = True
                self.dones[i] = 1
            
            # Store results
            states.append(new_state)
            rewards.append(reward)
            dones.append(done)
            # Update grid tensor for next step
            self.grid_tensors[i] = new_state
        
        return (
            torch.stack(states),
            torch.tensor(rewards, dtype=torch.float32),
            torch.tensor(dones, dtype=torch.bool),
        )
    
    def replace_done_episodes(self, dones: torch.Tensor):
        """
        Replace environments that are done with new random samples
        
        Args:
            dones: [batch_size] tensor of done flags
        """
        for i in range(self.batch_size):
            if dones[i]:
                target_grid = random.sample(self.target_grids[random.choice(range(4))])
                self._initialize_single_environment(i, target_grid)
    
    def get_current_states(self) -> torch.Tensor:
        """Get current states for all environments"""
        return torch.stack(self.grid_tensors)
    
    def get_batch_info(self, i) -> List:
        """Get info for all environments in batch"""
        return {
                'step_count': self.step_counts[i],
                'max_len': self.max_lens[i],
                'num_shapes': len(np.unique(self.target_grids_batch[i])[np.unique(self.target_grids_batch[i]) != 0]),
                'current_grid_shape': self.current_grids[i].shape,
                'target_grid_shape': self.target_grids_batch[i].shape
            }