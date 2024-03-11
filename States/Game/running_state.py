import pygame
from Utilities.settings import *
from .game_state import GameState
from .pause_state import PauseState
from Entities.player import Player
from map import Map

class RunningState(GameState):
    def __init__(self, game) -> None:
        GameState.__init__(self, game)
        self.map = Map(self._game.width, self._game.height)
        self.player1 = Player(self.map.set_starting_postion(0, 0), 'player_1', PLAYER_1_CONTROLS, (8, 7, 4), 32, 32, 2.2, self.map, self._game.screen)
        self.player2 = Player(self.map.set_starting_postion(0, 24), 'player_1', PLAYER_2_CONTROLS, (8, 7, 4), 32, 32, 2.2, self.map, self._game.screen)
        
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
                        self._game.fullscreen = not self.__fullscreen
                        if self._game.fullscreen:
                            self.handle_fullscreen()
        
    def update(self, delta_time) -> None:
        self.map.render_map(self._game.screen)
        self._game.draw_text('PLAYER 1', (100 * self._game.width // self._game.width), (20 * self._game.height // self._game.height))
        
        self.handle_events()
        
        pressed_keys = pygame.key.get_pressed()
        
        for player in self.map.get_players():
            player.update(pressed_keys, delta_time)
        