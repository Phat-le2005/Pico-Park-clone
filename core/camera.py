import pygame

class camerase:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

  
    def apply(self, target):
        return target.rect.move(-self.camera.x, -self.camera.y)

    def apply_rect(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)


    def update(self, players, map_width, map_height, screen_width, screen_height):
        # Lấy trung bình vị trí các player để làm tâm camera
        if not players:
            return

        # Trung bình vị trí các người chơi
        x = sum([p.rect.centerx for p in players]) // len(players)
        y = sum([p.rect.centery for p in players]) // len(players)

        # Camera sẽ di chuyển để giữ nhân vật ở giữa màn hình
        x -= screen_width // 2
        y -= screen_height // 2

        # Giới hạn camera không đi ra ngoài bản đồ
        x = max(0, min(x, map_width - screen_width))
        y = max(0, min(y, map_height - screen_height))

        self.camera = pygame.Rect(x, y, screen_width, screen_height)



        