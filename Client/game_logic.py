import pygame
from core.player import Player
from core.map import renderMap
from core.camera import camerase
from Server.configsever import SCREEN_WIDTH, SCREEN_HEIGHT

class GameLogic:
    def __init__(self, init_data):
        self.player_id = init_data["player_id"]
        color = init_data["color"]
        x, y = init_data["x"], init_data["y"]

        self.main_player = Player(x, y, color)
        self.other_players = {}
        self.players_data = {}

        # Load tilemap và camera
        self.tile_map = renderMap("TileSet_Map/Mario_Test_Map_Cao15.tmx")
        map_w = self.tile_map.tmx_data.width * self.tile_map.tmx_data.tilewidth
        map_h = self.tile_map.tmx_data.height * self.tile_map.tmx_data.tileheight #load map
        self.camera = camerase(map_w, map_h)

    def update_from_server(self, state_data):
        self.players_data = state_data #du lieu toan bo nguoi choi

    def get_input(self):
        keys = pygame.key.get_pressed()
        inputs = []
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            inputs.append("LEFT")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            inputs.append("RIGHT")
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            inputs.append("UP")
        else:
            inputs.append("OTHER")
        return inputs

    def update_players(self):
        if not self.players_data:
            return

        # Cập nhật player chính
        if str(self.player_id) in self.players_data:
            pdata = self.players_data[str(self.player_id)]
            self.main_player.rect.topleft = (pdata["x"], pdata["y"])
            self.main_player.set_state(pdata.get("state", "stand"))
            self.main_player.flip = pdata.get("flip", False)
            self.main_player.update()

        # Cập nhật camera
        self.camera.update([self.main_player], 
                           self.tile_map.tmx_data.width * self.tile_map.tmx_data.tilewidth,
                           self.tile_map.tmx_data.height * self.tile_map.tmx_data.tileheight,
                           SCREEN_WIDTH, SCREEN_HEIGHT)

        # Cập nhật các player khác
        for pid, pdata in self.players_data.items():
            if int(pid) == self.player_id:
                continue
            if pid not in self.other_players:
                self.other_players[pid] = Player(pdata["x"], pdata["y"], pdata["color"]) #Neu id ko co trong nguoi chs se tao 1 nguoi choi khac
            p = self.other_players[pid]
            p.rect.topleft = (pdata["x"], pdata["y"])
            p.set_state(pdata.get("state", "stand"))
            p.flip = pdata.get("flip", False)
            p.update()