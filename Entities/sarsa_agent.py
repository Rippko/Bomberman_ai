import pygame
import numpy as np
from Entities.ai_player import AiPlayer
from map import Map, Action
import random
import time
import pickle

class SARSA_agent(AiPlayer):
    def __init__(self, coords: tuple, entity_name: str, n_frames: tuple, s_width: int, s_height: int, scale, map: Map, game_display: pygame.display):
        super().__init__(coords, entity_name, n_frames, s_width, s_height, scale, map, game_display)
        self.alpha = 0.1
        self.gamma = 0.7
        self.epsilon = 0.1
        self.num_of_episodes = 0
        self.done = False
        self.decision_interval = 0.4
        self.last_decision_time = time.time()
        
        self.map_env = map
        self.action_map = {
            Action.MOVE_LEFT: self._move_left,
            Action.MOVE_RIGHT: self._move_right,
            Action.MOVE_UP: self._move_up,
            Action.MOVE_DOWN: self._move_down,
            Action.STOP_MOVE: self._stop_move,
            Action.PLACE_BOMB: self.place_bomb
        }
        #base je 5 akcí * 16 variant co se může stát tedy 16*5
        self.num_states = len(self.action_map) * 162
        self.num_actions = len(self.action_map)

        if not self.load_Q_table('Q_table.pkl'):
            self.Q_table = {}
            print('Q table not loaded')
        
    def save_Q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.Q_table, f)
        
    def load_Q_table(self, filename) -> bool:
        try:
            with open(filename, 'rb') as file:
                self.Q_table = pickle.load(file)
                print(self.Q_table)
            return True
        except FileNotFoundError:
            print(f"Error: File not found - {filename}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = random.choice(list(self.action_map.keys()))
        else:
            action = Action(np.argmax(self.Q_table[state]))
        return action

    def update_q_table(self, state, action, reward, next_state, next_action):
        #self.load_Q_table('Q_table.pkl')
        predict = self.Q_table[state][action.value]
        target = reward + self.gamma * self.Q_table[next_state][next_action.value]
        self.Q_table[state][action.value] += self.alpha * (target - predict)
        self.save_Q_table('Q_table.pkl')

    def learn(self, initial_state):
        state = initial_state
        if state not in self.Q_table.keys():
            self.Q_table[state] = [0] * self.num_actions
        action = self.choose_action(state)
        next_state, reward, self.done, info = self.map_env.step(action, state, self)
        print(f'Action: {action}, State: {state}, reward: {reward} for q_table: {self.Q_table[state]}')
        
        if next_state not in self.Q_table.keys():
            self.Q_table[next_state] = [0] * self.num_actions
        next_action = self.choose_action(next_state)
        self.update_q_table(state, action, reward, next_state, next_action)
    
    def update(self, delta_time):
        if self.done:
            self.save_Q_table('Q_table.pkl')
            self.done = False
        else:
            current_time = time.time()
            if current_time - self.last_decision_time > self.decision_interval:
                self.learn(self.map_env.get_map_state(self._get_position_in_grid(self.x, self.y)))
                self.last_decision_time = current_time
            super().update(delta_time)