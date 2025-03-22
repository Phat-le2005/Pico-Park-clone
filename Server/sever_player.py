from Collision.collision_map import CollisionMap
import pygame

class ServerPlayer:
    def __init__(self, x, y, color, collision_map):
        self.x = x
        self.y = y
        self.color = color

        self.vel_y = 0 # vận tốc chiều dọc
        self.gravity = 0.5 # trọng lực
        self.jump_power = -12 # lực nhảy
        self.max_fall_speed = 15 # tốc độ rơi max
        self.is_jumping = False
        self.jump_origin = y # tọa độ ban đàu trước khi nhảy
        self.speed = 4

        self.state = "stand"
        self.flip = False # xác định quya trái/ phải
        self.collision_map = collision_map
        self.width = 72
        self.height = 90
        self.on_ground = False # kiểm tra đã đứNg trên block chưa

    def handle_input(self, inputs):
        dx = 0

        if "LEFT" in inputs:
            dx = -self.speed
            self.flip = True
        elif "RIGHT" in inputs:
            dx = self.speed
            self.flip = False

        new_x = self.x + dx
        if not self.collides_x(new_x):
            self.x = new_x

        # Xử lý nhảy trước
        if "UP" in inputs and self.on_ground:
            self.is_jumping = True
            self.vel_y = self.jump_power
            self.jump_origin = self.y
            self.state = "jump"
            self.on_ground = False
            return  # không xử lý walk/stand trong frame này

        # Nếu không nhảy, xử lý walk/stand
        if self.on_ground:
            if dx != 0:
                self.state = "walk"
            else:
                self.state = "stand"

    def update(self):
        self.vel_y += self.gravity
        if self.vel_y > self.max_fall_speed:
            self.vel_y = self.max_fall_speed

        future_y = self.y + self.vel_y
        if self.collides_y(future_y):
            if self.vel_y > 0:
                player_rect = pygame.Rect(self.x, future_y, self.width, self.height)
                min_top = None
                for rect in self.collision_map.solid_objects:
                    if player_rect.colliderect(rect):
                        if min_top is None or rect.top < min_top:
                            min_top = rect.top
                if min_top is not None:
                    self.y = int(min_top - self.height) # kiểm tra chân nhân vật đã trùng với block chưa
            self.vel_y = 0
            self.is_jumping = False
            self.on_ground = True   
        else:
            self.y = future_y
            self.on_ground = False #kiểm tra đụng đầu

        # Chỉ xử lý trạng thái khi không đứng đất
        if not self.on_ground:
            if self.vel_y < 0:
                self.state = "jump"
            elif self.vel_y > 0:
                if self.state != "walk":
                    self.state = "fall"
        print(f"[DEBUG] y: {self.y:.2f}, vel_y: {self.vel_y:.2f}, on_ground: {self.on_ground}, state: {self.state}")

    def collides_x(self, new_x):
        buffer=1
        player_rect = pygame.Rect(int(new_x),int(self.y), self.width+1, self.height)
        for rect in self.collision_map.solid_objects:
            if player_rect.colliderect(rect):
                return True
        return False    #kiểm tra chướNg ngại vật theo chiều ngang

    def collides_y(self, new_y): #kiểm tra chướNg ngại vật theo chiều dọc
        buffer = 1  # chấp nhận lệch nhỏ
        player_rect = pygame.Rect(int(self.x), int(new_y), self.width, self.height+1)
        for rect in self.collision_map.solid_objects:
            if player_rect.colliderect(rect):
                return True
        return False

    def get_state(self):
        return {
            "x": int(self.x),
            "y": int(self.y),
            "color": self.color,
            "state": self.state, #gói dữ liệu truyền lên server
            "flip": self.flip
        }
