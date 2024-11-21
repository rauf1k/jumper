import pygame
import sys
import random

from player import Player
from obstacles import MAX_GAP, MIN_GAP, Obstacle
from powerup import PowerUp


WIDTH, HEIGHT = 1200, 600
BG_COLOR = (230, 230, 230)
GROUND_COLOR = (50, 50, 50) 
FPS = 60


RECORD_FILE = 'highscore.txt'

icon = pygame.image.load('assest/sprite0.png') 
pygame.display.set_icon(icon)

def load_highscore():
    try:
        with open(RECORD_FILE, 'r') as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(highscore):
    with open(RECORD_FILE, 'w') as file:
        file.write(str(highscore))

def show_instructions(screen):
    font = pygame.font.Font(None, 36)
    instructions = [
        "Instructions:",
        "Space: Jump ",
        "W: Super Jump (must collect powerups)",
        "R: Restart the game",
    ]
    y_offset = 50
    for line in instructions:
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_offset))
        y_offset += 40

    
    pygame.mixer.init()



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Пригун")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    
    pygame.mixer.init()

    
    music_night = "assest/night.mp3"
    music_day = "assest/day.mp3"
    pygame.mixer.music.set_volume(0.1)  

    
    current_music = None  

   
    background1 = pygame.image.load("assest/background.jpg").convert()
    background2 = pygame.image.load("assest/background2.jpg").convert()

    background1 = pygame.transform.scale(background1, (WIDTH, HEIGHT))
    background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))

    
    GROUND_COLORS = [(50, 50, 50), (150, 150, 150)]  
    OBSTACLE_COLORS = [(150, 75, 0), (50, 50, 50)]  

    
    current_bg_index = 0

    
    player = Player()
    obstacles = []
    powerups = []
    
    
    game_speed = 5
    score = 0
    highscore = load_highscore()
    distance_traveled = 0
    game_active = True
    show_help = True
    last_was_high = False
    high_obstacle_count = 0


    while True:
        
        current_bg_index = (score // 30) % 2  
        current_background = [background1, background2][current_bg_index]
        current_ground_color = GROUND_COLORS[current_bg_index]
        current_obstacle_color = OBSTACLE_COLORS[current_bg_index]

        
        if current_background == background1 and current_music != music_night:
            pygame.mixer.music.load(music_night)
            pygame.mixer.music.play(-1)  
            current_music = music_night
        elif current_background == background2 and current_music != music_day:
            pygame.mixer.music.load(music_day)
            pygame.mixer.music.play(-1)  
            current_music = music_day

        
        if show_help and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            current_music = None

        
        if not game_active and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            current_music = None
        
        current_bg_index = (score // 30) % 2  
        current_background = [background1, background2][current_bg_index]
        current_ground_color = GROUND_COLORS[current_bg_index]
        current_obstacle_color = OBSTACLE_COLORS[current_bg_index]

        
        screen.blit(current_background, (0, 0))

        
        pygame.draw.rect(screen, current_ground_color, (0, 550, WIDTH, HEIGHT - 550))

        
        for obstacle in obstacles:
            pygame.draw.rect(screen, current_obstacle_color, obstacle.rect)


        if show_help:
            show_instructions(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        show_help = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    player.start_jump()
                elif event.key == pygame.K_w and game_active and player.has_super_jump():
                    player.use_super_jump()
                elif event.key == pygame.K_r and not game_active:
                    
                    game_active = True
                    score = 0
                    game_speed = 5
                    distance_traveled = 0
                    player.reset()
                    obstacles.clear()
                    powerups.clear()
                    high_obstacle_count = 0

        if game_active:
            
            player.update()

            
            if len(obstacles) == 0 or obstacles[-1].rect.right < WIDTH - random.randint(MIN_GAP, MAX_GAP):
                new_obstacle, last_was_high, high_obstacle_count = Obstacle.generate_random_obstacle(
                    player, WIDTH, score, last_was_high, high_obstacle_count
                )
                obstacles.append(new_obstacle)

            
            for obstacle in obstacles:
                obstacle.update(game_speed)
                obstacle.draw(screen, current_obstacle_color)  


                
                if obstacle.rect.colliderect(player.rect):
                    game_active = False

                
                if obstacle.rect.right < 0:
                    obstacles.remove(obstacle)
                    score += 1

            
            if score % 5 == 0 and score > 0 and len(powerups) == 0:
                new_powerup = PowerUp.generate_powerup_between_obstacles(obstacles, WIDTH)
                if new_powerup:
                    powerups.append(new_powerup)

            
            for powerup in powerups[:]:
                powerup.update(game_speed)
                powerup.draw(screen)

                
                if powerup.rect.colliderect(player.rect):
                    player.collect_super_jump()
                    powerups.remove(powerup)

                
                if powerup.rect.right < 0:
                    powerups.remove(powerup)

            
            distance_traveled += game_speed / 60  
            distance_text = font.render(f"Distance: {int(distance_traveled)}", True, (255, 255, 255))
            highscore_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
            super_jump_text = font.render(f"Super Jumps: {player.super_jump_count}", True, (255, 255, 255))
            screen.blit(distance_text, (10, 10))
            screen.blit(highscore_text, (10, 40))
            screen.blit(super_jump_text, (10, 70))

            
            if int(distance_traveled) % 150 == 0 and int(distance_traveled) > 0:
                game_speed += 0.1

            
            player.draw(screen)

        else:
            
            game_over_text = font.render("Game Over! Press 'R' to Restart", True, (0, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

            
            if int(distance_traveled) > highscore:
                highscore = int(distance_traveled)
                save_highscore(highscore)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()