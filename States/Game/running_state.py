import pygame
from Utilities.settings import *
from .game_state import GameState
from .pause_state import PauseState
from Entities.player import Player
from Entities.sarsa_agent import SARSA_agent
from Q_table import Q_table
from map import Map
import time

class RunningState(GameState):
    def __init__(self, game) -> None:
        GameState.__init__(self, game)
        self.epsilon = 0.8
        self.episodes = 0
        self._q_table = Q_table('Q_table.pkl')
        self.initialize()
        
    def initialize(self) -> None:
        self.map = Map(self._game.width, self._game.height)
        self._q_table.load_Q_table()
        self.player1 = Player(self.map.set_starting_postion(0, 0), 'player_1', PLAYER_1_CONTROLS, (8, 7, 4), 32, 32, 2.2, self.map, self._game.screen)
        self.sarsa_agent2 = SARSA_agent(self.map.set_starting_postion(0, 24), 'player_2', (8, 7, 4), 32, 32, 2.2, self.map, self._q_table, self._game.screen)
        self.sarsa_agent3 = SARSA_agent(self.map.set_starting_postion(12, 0), 'player_3', (8, 7, 4), 32, 32, 2.2, self.map,  self._q_table, self._game.screen)
        self.sarsa_agent4 = SARSA_agent(self.map.set_starting_postion(12, 24), 'player_4', (8, 7, 4), 32, 32, 2.2, self.map,  self._q_table, self._game.screen)
        
        self.all_players = self.map.get_players()
        
        if self.epsilon is not None:
            for player in self.all_players:
                if type(player) == SARSA_agent and player.epsilon > 0.4:
                    player.epsilon = self.epsilon
                    print(f'\033[32mEpsilon: {self.epsilon}\033[0m')

        
    
    def handle_events(self) -> None:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        new_state = PauseState(self._game)
                        new_state.enter_state()
                    if event.key == pygame.K_f:
                        self._game.fullscreen = not self._game.fullscreen
                        if self._game.fullscreen:
                            self._game.handle_fullscreen()
                        else:
                            self._game.screen = pygame.display.set_mode((self._game.width, self._game.height))
        
    def update(self, delta_time) -> None:
        self.map.render_map(self._game.screen, delta_time)
        self.handle_events()
        
        pressed_keys = pygame.key.get_pressed()
        
        dead_players = 0
        for player in self.all_players:
            if player._current_state == player.states['Dying'] and player._current_frame == len(player._all_actions[player._current_state.get_name()]['front']) - 1:
                dead_players += 1
                
        if dead_players >= len(self.all_players) - 1:
            self._q_table.save_Q_table()
            self.initialize()

        if self.episodes == 150000:
            self.epsilon -= 0.05
            for player in self.all_players:
                if type(player) == SARSA_agent and player.epsilon > 0.2:
                    player.epsilon = self.epsilon
                    print(f'\033[32mEpsilon: {self.epsilon}\033[0m')
            self.episodes = 0
                
        for player in self.all_players:
            if type(player) == SARSA_agent:
                player.update(delta_time)
            else:
                player.update(pressed_keys, delta_time)

        self.episodes += 1