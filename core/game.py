import pygame
from core.playertest import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.players = [
            Player(100, 100, (255, 0, 0)),   # Đỏ
            Player(200, 100, (0, 255, 0)),   # Xanh lá
        ]

    def update(self):
        keys = pygame.key.get_pressed()
        self.players[0].handle_input(keys)  # Tạm thời: 1 người điều khiển bằng bàn phím

        for player in self.players:
            player.update()

    def draw(self):
        self.screen.fill((240, 240, 240))
        for player in self.players:
            player.draw(self.screen)
        pygame.display.flip()
