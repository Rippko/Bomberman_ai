import pygame
import numpy as np
from Entities.ai_player import AiPlayer
from map import Map

class SARSA_agent(AiPlayer):
    def __init__(self, coords: tuple, entity_name: str, n_frames: tuple, s_width: int, s_height: int, scale, map: Map, game_display: pygame.display):
        super().__init__(coords[0], coords[1], entity_name=entity_name, n_frames=n_frames, s_width=s_width, s_height=s_height, scale=scale, map=map, game_display=game_display)
        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 0.1
        self.map_env = map
        self.action_map = {
            'move_left': self.move_left,
            'move_right': self.move_right,
            'move_up': self.move_up,
            'move_down': self.move_down,
            'place_bomb': self.place_bomb
        }
        self.num_states = 390625
        self.num_actions = len(self.action_map)
        if not self.load_Q_table('Q_table.npy'):
            self.Q_table = np.random.uniform(low=-1, high=1, size=(self.num_states, self.num_actions))
        
    def save_Q_table(self, filename):
        np.save(filename, self.Q_table)
        
    def load_Q_table(self, filename) -> bool:
        self.Q_table = np.load(filename)
        if np.load(filename).shape == self.Q_table.shape:
            print('Q-table loaded successfully.')
            return True
        else:
            print('Q-table loaded with incorrect shape.')
            return False

    def choose_action(self, state):
        """ Choose an action using the epsilon-greedy policy. """
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice(self.num_actions)
        else:
            action = np.argmax(self.Q_table[state])
        return action

    def update(self, state, action, reward, next_state, next_action):
        """ Update Q-values using the SARSA formula. """
        predict = self.Q_table[state, action]
        target = reward + self.gamma * self.Q_table[next_state, next_action]
        self.Q_table[state, action] += self.alpha * (target - predict)

    def learn(self, initial_state):
        """ Implement the SARSA learning process within the environment. """
        state = initial_state
        action = self.choose_action(state)
        done = False
        while not done:
            self.action_map[action]()  # Perform the action using AiPlayer methods
            next_state, reward, done, info = self.map_env.step(action)  # Get the environment's new state and reward
            next_action = self.choose_action(next_state)
            self.update(state, action, reward, next_state, next_action)
            state = next_state
            action = next_action
            