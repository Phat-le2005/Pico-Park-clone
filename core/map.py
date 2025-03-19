import pygame
import pytmx
from pytmx.util_pygame import load_pygame

class renderMap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
  
    def draw(self, screen, camera):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        pos = (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                        screen.blit(tile, camera.apply(pygame.Rect(pos, (0, 0))))