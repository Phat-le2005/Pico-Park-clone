import pygame
import os
class Player:
    def __init__(self,x,y,color):
        self.animations = {
            "stand": self.load_frames("p1_stand", 1),   # 1 → số frame idle
            "walk": self.load_frames("p1_walk", 11),  # 11 frame đi bộ
            "jump": self.load_frames("p1_jump", 1)    # 1 hoặc bao nhiêu frame bạn có
        }
        self.state = "stand"
        self.image = self.animations[self.state][0]
        self.current_frame = 0
        self.frame_delay = 5
        self.frame_counter = 0
        self.flip = True
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vel = 4
        self.is_jumping = False
        self.jump_height = 30        
        self.jump_speed = 4          
        self.jump_origin = 0 
        self.vel_y = 0              # tốc độ rơi/nhảy theo Y
        self.gravity = 0.5          # trọng lực
        self.jump_power = -10       # lực nhảy (âm vì đi lên)
        self.max_fall_speed = 10   

    def load_frames(self, folder_name, frame_count):
        frames = []
        folder_path = f"asset/Player/{folder_name}/PNG"
        for i in range(1, frame_count + 1):
            filename = f"{folder_name}{str(i).zfill(2)}.png"
            full_path = os.path.join(folder_path, filename)
            image = pygame.image.load(full_path).convert_alpha()
            frames.append(image)
        return frames

    def set_state(self, new_state):
        if new_state != self.state:
            self.state = new_state
            self.current_frame = 0
            self.frame_counter = 0

    def update(self):
        frames = self.animations[self.state]
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.frame_counter = 0
        self.image = frames[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.is_jumping:
            self.rect.y += self.vel_y  # di chuyển theo tốc độ

            # Tăng tốc độ rơi theo gravity
            self.vel_y += self.gravity

            # Giới hạn tốc độ rơi
            if self.vel_y > self.max_fall_speed:
                self.vel_y = self.max_fall_speed

            # Đến điểm tiếp đất (giả định ground ở y = self.jump_origin)
            if self.rect.y >= self.jump_origin:
                self.rect.y = self.jump_origin
                self.is_jumping = False
                self.vel_y = 0
                self.set_state("stand")
    def handle_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.vel
            self.flip = True
            self.set_state("walk")
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.vel
            self.flip = False
            self.set_state("walk")
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            if not self.is_jumping:
                self.is_jumping = True
                self.is_jumping = True
                self.vel_y = self.jump_power
                self.jump_origin = self.rect.y
                self.set_state("jump")
        else:
            self.set_state("stand")

