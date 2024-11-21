import pygame
import os




GRAVITY = 0.6
MAX_JUMP_HEIGHT = 40  
BASE_JUMP_VELOCITY = -15  
SUPER_JUMP_MULTIPLIER = 1.75  


FRAME_DELAY = 5

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 500, 30, 50)  
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_held_time = 0
        self.super_jump_count = 0

        try:
            original_frames = [
                pygame.image.load(os.path.join("assest", "sprite0.png")).convert_alpha(),
                pygame.image.load(os.path.join("assest", "sprite1.png")).convert_alpha(),
                pygame.image.load(os.path.join("assest", "sprite2.png")).convert_alpha()
            ]
            
            self.frames = [
                pygame.transform.scale(frame, (int(self.rect.width * 1.7), int(self.rect.height * 1.1)))
                for frame in original_frames
            ]
        except FileNotFoundError as e:
            print(f"Error loading sprite: {e}")
            raise


        self.current_frame = 0  
        self.animation_timer = 0.1  
        self.on_ground_frame = self.frames[0]  
        self.jump_frame = self.frames[2]  

    def start_jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_held_time = 0
            self.velocity_y = BASE_JUMP_VELOCITY  

    def update(self):
        keys = pygame.key.get_pressed()
        if self.is_jumping:
            if keys[pygame.K_SPACE]:
                self.jump_held_time += 1

                
                if self.jump_held_time * abs(BASE_JUMP_VELOCITY) * GRAVITY < MAX_JUMP_HEIGHT:
                    self.velocity_y -= 0.5  
                else:
                    self.velocity_y = min(self.velocity_y, -BASE_JUMP_VELOCITY)  

       
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        
        if self.rect.bottom > 550:
            self.rect.bottom = 550
            self.is_jumping = False
            self.velocity_y = 0

        
        if not self.is_jumping:
            self.animation_timer += 1
            if self.animation_timer >= FRAME_DELAY:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        
        if self.is_jumping:
            screen.blit(self.jump_frame, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.frames[self.current_frame], (self.rect.x, self.rect.y))

    def has_super_jump(self):
        return self.super_jump_count > 0

    def use_super_jump(self):
        if self.super_jump_count > 0 and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = BASE_JUMP_VELOCITY * SUPER_JUMP_MULTIPLIER
            self.super_jump_count -= 1

    def collect_super_jump(self):
        self.super_jump_count += 1

    def reset(self):
        self.rect = pygame.Rect(100, 500, 30, 50)
        self.velocity_y = 0
        self.is_jumping = False
        self.super_jump_count = 0
        self.current_frame = 0
        self.animation_timer = 0
