# 📁 game_client.py (entrypoint)
from Client.network_client import NetworkClient
from Client.game_logic import GameLogic
from Client.renderer import GameRenderer
from Server.configsever import *
import pygame, sys

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Kết nối tới server
network = NetworkClient(HOST, PORT)
init_data = network.wait_for_init()

# Tạo logic + renderer
logic = GameLogic(init_data) # tao nguoi choi
renderer = GameRenderer(screen, logic.main_player, logic.other_players, logic.camera, logic.tile_map) # render cua so moi cho nguoi choi moi

# Bắt đầu nhận dữ liệu từ server
network.start_receiving(callback=logic.update_from_server) #nhan du lieu state tu sever

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            network.close()
            pygame.quit()
            sys.exit()

    # Gửi input
    inputs = logic.get_input()
    network.send_input(inputs)

    # Update animation
    logic.update_players()

    # Render
    renderer.render()

    pygame.display.flip()
    clock.tick(FPS)