# 📁 client/renderer.py
import pygame
from Server.configsever import SCREEN_WIDTH, SCREEN_HEIGHT

class GameRenderer:
    def __init__(self, screen, main_player, other_players, camera, tile_map):
        self.screen = screen
        self.main_player = main_player #player chinh
        self.other_players = other_players #tat ca player
        self.camera = camera
        self.tile_map = tile_map
        self.font = pygame.font.SysFont(None, 28)

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen

        # Vẽ tilemap trước
        self.tile_map.draw(self.screen, self.camera)

        # Vẽ các người chơi
        for pid, p in self.other_players.items():
            self.screen.blit(p.image, self.camera.apply(p))

        # Vẽ người chơi chính sau cùng (trên cùng)
        self.screen.blit(self.main_player.image, self.camera.apply(self.main_player))

        # (Optional) Có thể vẽ tên người chơi, key HUD,... tại đây sau này

    def render_waiting_message(self, message="⏳ Đang chờ server gửi dữ liệu..."):
        msg = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2,
                               SCREEN_HEIGHT // 2 - msg.get_height() // 2))
