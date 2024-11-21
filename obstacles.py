import pygame
import random


OBSTACLE_WIDTH = 15  
MIN_OBSTACLE_HEIGHT = 50  
MAX_OBSTACLE_HEIGHT = 150  
HIGH_OBSTACLE_HEIGHT = 400  
MIN_GAP = 200  
MAX_GAP = 500  

class Obstacle:
    def __init__(self, x, height):
        self.rect = pygame.Rect(x, 550 - height, OBSTACLE_WIDTH, height)

    @staticmethod
    def generate_random_obstacle(player, screen_width, score, last_was_high=False, high_obstacle_count=0):
        if last_was_high or high_obstacle_count >= 3:
            
            height = random.randint(MIN_OBSTACLE_HEIGHT, MAX_OBSTACLE_HEIGHT)
            return Obstacle(screen_width + random.randint(MIN_GAP, MAX_GAP), height), False, max(high_obstacle_count - 1, 0)

        if score >= 15:
            
            chance = random.randint(1, 4)  
            if chance == 1: 
                height = HIGH_OBSTACLE_HEIGHT
                return Obstacle(screen_width + random.randint(MIN_GAP, MAX_GAP), height), True, high_obstacle_count + 1
            else:
                height = random.randint(MIN_OBSTACLE_HEIGHT, MAX_OBSTACLE_HEIGHT)
                return Obstacle(screen_width + random.randint(MIN_GAP, MAX_GAP), height), False, 0
        else:
            
            height = random.randint(MIN_OBSTACLE_HEIGHT, MAX_OBSTACLE_HEIGHT)
            return Obstacle(screen_width + random.randint(MIN_GAP, MAX_GAP), height), False, 0

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
