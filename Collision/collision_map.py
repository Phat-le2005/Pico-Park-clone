import pytmx
import pygame

class CollisionMap:
    def __init__(self, file):
        self.data = pytmx.TiledMap(file)
        self.tileWidth = self.data.tilewidth
        self.tileHeight = self.data.tileheight
        self.width = self.data.width
        self.height = self.data.height

        # self.solid = self.getSolid()
        # self.solid_map = self._build_collision_grid()
        self.solid_objects = self._get_solid_objects()

    # def getSolid(self):
    #     solid = set()
    #     for id, tile in self.data.tile_properties.items():
    #         props = tile or {}
    #         if props.get("solid", False): 
    #             solid.add(id)
    #     return solid

    # def _build_collision_grid(self):
    #     grid = [[False for _ in range(self.width)] for _ in range(self.height)]
    #     for layer in self.data.visible_layers:
    #         if isinstance(layer, pytmx.TiledTileLayer): 
    #             for x, y, gid in layer.iter_data():
    #                 if gid in self.solid:
    #                     grid[y][x] = True 
    #     return grid

    def _get_solid_objects(self):
        solid_objects = []
        for layer in self.data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "Triggers":
                for obj in layer:
                    if obj.properties.get("Solid", False):
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        # print("[DEBUG] Object solid loaded:", rect)
                        solid_objects.append(rect)
        return solid_objects #tao cac khoi vat can

    def is_solid_pixel(self, x, y):
        tile_x = int(x // self.tileWidth) # chuyen coi dung o vuong thu may
        tile_y = int(y // self.tileHeight)
        if 0 <= tile_x < self.width and 0 <= tile_y < self.height:
            if self.solid_map[tile_y][tile_x]:
                return True
        for rect in self.solid_objects:
            if rect.collidepoint(x, y):
                return True
        return False