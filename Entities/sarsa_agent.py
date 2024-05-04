import pygame
import numpy as np
from Entities.ai_player import AiPlayer
from map import Map, Action
import random
import time
import Q_table
import pickle

class SARSA_agent(AiPlayer):
    def __init__(self, coords: tuple, entity_name: str, n_frames: tuple, s_width: int, s_height: int, scale, map: Map, Q_table: Q_table, game_display: pygame.display):
        super().__init__(coords, entity_name, n_frames, s_width, s_height, scale, map, game_display)
        self.alpha = 0.1
        self.gamma = 0.7
        self.epsilon = 0.1
        self.done = False
        self.decision_interval = 0.2
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
        self.num_actions = len(self.action_map)

        self.Q_table = Q_table

    def choose_action(self, state) -> Action:
        if np.random.uniform(0, 1) < self.epsilon:
            if len(self._bombs) < self._max_bombs:
                action = random.choice(list(self.action_map.keys()))
            else:
                action = random.choice(list(self.action_map.keys())[:-1])
        else:
            if len(self._bombs) < self._max_bombs:
                action = Action(np.argmax(self.Q_table.data[state]))
            else:
                action = Action(np.argmax(self.Q_table.data[state][:-1]))
        return action

    def update_q_table(self, state, action, reward, next_state, next_action) -> None:
        predict = self.Q_table.data[state][action.value]
        target = reward + self.gamma * self.Q_table.data[next_state][next_action.value]
        self.Q_table.data[state][action.value] += self.alpha * (target - predict)

    def learn(self, initial_state) -> None:
        state = initial_state
        if state not in self.Q_table.data.keys():
            self.Q_table.data[state] = [0] * self.num_actions
        action = self.choose_action(state)
        next_state, reward, self.done, info = self.map_env.step(action, state, self)
        print(f'PLAYER: {self._entity_name} ,Action: {action}, State: {state}, reward: {reward} for q_table: {self.Q_table.data[state]}')
        
        if next_state not in self.Q_table.data.keys():
            self.Q_table.data[next_state] = [0] * self.num_actions
        next_action = self.choose_action(next_state)
        self.update_q_table(state, action, reward, next_state, next_action)
        
    def update(self, delta_time) -> None:
        if not self.done:
            current_time = time.time()
            if current_time - self.last_decision_time > self.decision_interval:
                self.learn(self.map_env.get_map_state(self))
                self.last_decision_time = current_time
        super().update(delta_time)