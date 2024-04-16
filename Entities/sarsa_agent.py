import pygame
import numpy as np
from Entities.ai_player import AiPlayer
from map import Map
import random
import time

class SARSA_agent(AiPlayer):
    def __init__(self, coords: tuple, entity_name: str, n_frames: tuple, s_width: int, s_height: int, scale, map: Map, game_display: pygame.display):
        super().__init__(coords, entity_name, n_frames, s_width, s_height, scale, map, game_display)
        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 0.4
        self.done = False
        self.decision_interval = 1
        self.last_decision_time = time.time()
        
        self.map_env = map
        self.action_map = {
            0: self._move_left,
            1: self._move_right,
            2: self._move_up,
            3: self._move_down,
            4: self._stop_move,
            # 5: self.place_bomb
        }
        #390625
        self.num_states = 390625
        self.num_actions = len(self.action_map)
        self.base = self.num_actions
        if not self.load_Q_table('Q_table.npy'):
            self.Q_table = np.random.uniform(low=-1, high=1, size=(self.num_states, self.num_actions))
            
    def state_to_index(self, state_vector):
        index = 0
        for value in state_vector:
            index = (index * self.base + value) % 390625
        return index
        
    def save_Q_table(self, filename):
        np.save(filename, self.Q_table)
        
    def load_Q_table(self, filename) -> bool:
        try:
            loaded_data = np.load(filename)  # Načti data jednou
            if loaded_data.shape == (self.num_states, self.num_actions):
                self.Q_table = loaded_data
                print('Q-table loaded successfully.')
                return True
            else:
                print('Q-table loaded with incorrect shape.')
                return False
        except FileNotFoundError:
            return False
        except Exception as e:
            return False

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = random.choice(list(self.action_map.keys()))
            print('Random action:', action)
        else:
            action_index = np.argmax(self.Q_table[state, :])
            action = list(self.action_map.keys())[action_index]
            print('Best action:', action)
        return action

    def update_q_table(self, state, action, reward, next_state, next_action):
        predict = self.Q_table[state, action]
        target = reward + self.gamma * self.Q_table[next_state, next_action]
        self.Q_table[state, action] += self.alpha * (target - predict)
        self.save_Q_table('Q_table.npy')

    def learn(self, initial_state):
        state = self.state_to_index(self.map_env.get_map_state(self.get_position()))
        action = self.choose_action(state)
        next_state, reward, self.done, info = self.map_env.step(action, self)
        next_state = self.state_to_index(next_state)
        next_action = self.choose_action(next_state)
        self.update_q_table(state, action, reward, next_state, next_action)
        state = next_state
        action = next_action
    
    def update(self, delta_time):
        if self.done:
            self.save_Q_table('Q_table.npy')
            self.done = False
        else:
            current_time = time.time()
            if current_time - self.last_decision_time > self.decision_interval:
                self.learn(self.map_env.get_map_state(self.get_position()))
                self.last_decision_time = current_time
            super().update(delta_time)