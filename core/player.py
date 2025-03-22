import pygame
import os

class Player:
    def __init__(self, x, y, color):
        self.animations = {
            "stand": self.load_frames("p1_stand", 1),
            "walk": self.load_frames("p1_walk", 11),
            "jump": self.load_frames("p1_jump", 1),
            "fall": self.load_frames("p1_jump",1)
        }
        self.state = "stand"
        self.image = self.animations[self.state][0]
        self.current_frame = 0
        self.frame_delay = 5
        self.frame_counter = 0
        self.flip = False
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.color = color

    def load_frames(self, folder_name, frame_count):
        frames = []
        folder_path = f"asset/Player/{folder_name}/PNG"
        for i in range(1, frame_count + 1):
            filename = f"{folder_name}{str(i).zfill(2)}.png"
            full_path = os.path.join(folder_path, filename)
            if os.path.exists(full_path):
                image = pygame.image.load(full_path).convert_alpha()
                frames.append(image)
            else:
                print("[LỖI] Không tìm thấy:", full_path)
        return frames

    def set_state(self, new_state):
        if new_state != self.state:
            self.state = new_state
            self.current_frame = 0
            self.frame_counter = 0

    def update(self):
        frames = self.animations.get(self.state, self.animations["stand"])
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.frame_counter = 0
        self.image = frames[self.current_frame]
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)