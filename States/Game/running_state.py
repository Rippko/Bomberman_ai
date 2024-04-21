import pygame
from Utilities.settings import *
from .game_state import GameState
from .pause_state import PauseState
from Entities.player import Player
from Entities.sarsa_agent import SARSA_agent
from map import Map
import time

class RunningState(GameState):
    def __init__(self, game) -> None:
        GameState.__init__(self, game)
        self.initialize()
        
    def initialize(self) -> None:
        self.map = Map(self._game.width, self._game.height)
        self.player1 = Player(self.map.set_starting_postion(0, 0), 'player_1', PLAYER_1_CONTROLS, (8, 7, 4), 32, 32, 2.2, self.map, self._game.screen)
        self.sarsa_agent = SARSA_agent(self.map.set_starting_postion(0, 24), 'player_1', (8, 7, 4), 32, 32, 2.2, self.map, self._game.screen)

        self.all_players = self.map.get_players()
    
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
        
    def update(self, delta_time) -> None:
        self.map.render_map(self._game.screen, delta_time)
        self._game.draw_text('PLAYER 1', (100 * self._game.width // self._game.width), (20 * self._game.height // self._game.height))
            
        self.handle_events()
        
        pressed_keys = pygame.key.get_pressed()
        
        for player in self.all_players:
            if type(player) == SARSA_agent:
                if player.done:
                    player.save_Q_table('Q_table.npy')
                    self.initialize()
                player.update(delta_time)
            else:
                player.update(pressed_keys, delta_time)