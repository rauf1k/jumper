import pygame
import random

from obstacles import MIN_GAP


POWERUP_SIZE = 20  
POWERUP_COLOR = (255, 0, 0)  


STATIC_POWERUP_Y = 500  

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, POWERUP_SIZE, POWERUP_SIZE)

    @staticmethod
    def should_spawn_powerup(obstacle_count):
        if obstacle_count % 5 == 0 and obstacle_count > 0:
            return True
        return False

    @staticmethod
    def generate_powerup_between_obstacles(obstacles, screen_width):
        if len(obstacles) >= 2:
            for i in range(len(obstacles) - 1):
                gap = obstacles[i + 1].rect.left - obstacles[i].rect.right
                if gap >= MIN_GAP:
                    x = obstacles[i].rect.right + (gap // 2)
                    y = STATIC_POWERUP_Y  
                    return PowerUp(x, y)
        return PowerUp(screen_width, STATIC_POWERUP_Y)

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, POWERUP_COLOR, self.rect)
