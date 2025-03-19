import pygame
import sys

from Network.configsever import *
from core.map import renderMap
from core.camera import camerase
from core.player import Player

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TEST LOCAL - Pico Park")
    clock = pygame.time.Clock()

    # Load bản đồ
    tile_map = renderMap("TileSet_Map/Mario_Test_Map_Cao15.tmx")

    # Tạo camera và player
    camera = camerase(tile_map.tmx_data.width * tile_map.tmx_data.tilewidth,
                      tile_map.tmx_data.height * tile_map.tmx_data.tileheight)

    player = Player(300, 200, (255, 0, 0))  # Player màu đỏ dễ thấy

    # Vòng lặp game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Điều khiển bằng phím
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        # Cập nhật camera theo player
        camera.update([player],
                      tile_map.tmx_data.width * tile_map.tmx_data.tilewidth,
                      tile_map.tmx_data.height * tile_map.tmx_data.tileheight,
                      SCREEN_WIDTH, SCREEN_HEIGHT)

        # Vẽ
        screen.fill((0, 0, 0))
        tile_map.draw(screen, camera)
        player.update()
        screen.blit(player.image, camera.apply(player)) 

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
