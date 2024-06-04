import pygame
import random
import sys

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CosmoDartPy")

plane_img = pygame.image.load("plane.png").convert_alpha()
plane_img = pygame.transform.scale(plane_img, (50, 30))

obstacle_img = pygame.image.load("obstacle.png").convert_alpha()
obstacle_img = pygame.transform.scale(obstacle_img, (25, 25))  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = plane_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -7  
        if keys[pygame.K_RIGHT]:
            self.speed_x = 7  
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = obstacle_img  

        scale_factor = random.uniform(0.8, 1.2)  
        self.image = pygame.transform.scale(self.original_image, (int(self.original_image.get_width() * scale_factor), int(self.original_image.get_height() * scale_factor)))

        self.rotation = random.randint(0, 360)  
        self.image = pygame.transform.rotate(self.image, self.rotation)

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height

        self.speed_y = obstacle_speed  

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def check_collision_with_obstacles_and_player(new_obstacle, obstacles, player):
    for obstacle in obstacles:
        if new_obstacle.rect.colliderect(obstacle.rect):
            return True
    return False  

def game_over_screen(seconds):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(game_over_text, game_over_rect)
    time_text = font.render(f"Tempo: {seconds}s", True, WHITE)  
    time_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(time_text, time_rect)
    play_again_text = font.render("Jogar Novamente", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(play_again_text, play_again_rect)
    pygame.display.flip()
    return play_again_rect

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

background_img = pygame.image.load("background.png").convert()
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

start_ticks = pygame.time.get_ticks()  
font = pygame.font.Font(None, 36)  
game_over_time = None  

clock = pygame.time.Clock()
running = True
obstacle_speed = 2.5  
obstacle_frequency = 90  
game_time = 0  
obstacle_timer = 0  
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mx, my = pygame.mouse.get_pos()
            if play_again_rect.collidepoint(mx, my):
                all_sprites.empty()
                obstacles.empty()
                player.rect.centerx = SCREEN_WIDTH // 2
                player.rect.bottom = SCREEN_HEIGHT - 10
                all_sprites.add(player)
                start_ticks = pygame.time.get_ticks()
                game_time = 0
                obstacle_speed = 2.5
                obstacle_frequency = 90
                game_over = False
                game_over_time = None  
                obstacle_timer = 0

    if not game_over:
        all_sprites.update()

        obstacle_timer += 1
        if obstacle_timer >= 25 and random.randint(1, 100) <= obstacle_frequency:
            obstacle_timer = 0  

            obstacle = Obstacle()

            if not check_collision_with_obstacles_and_player(obstacle, obstacles, player):
                all_sprites.add(obstacle)
                obstacles.add(obstacle)

        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            game_over = True
            game_over_time = (pygame.time.get_ticks() - start_ticks) // 1000  
            play_again_rect = game_over_screen(game_over_time)

    screen.blit(background_img, (0, 0))  
    all_sprites.draw(screen)

    if not game_over:
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000

        timer_text = font.render(f"Tempo: {seconds}s", True, WHITE)
        screen.blit(timer_text, (10, 10))
    else:
        if game_over_time is not None:
            timer_text = font.render(f"Tempo: {game_over_time}s", True, WHITE)
            screen.blit(timer_text, (10, 10))

    if game_over:
        play_again_rect = game_over_screen(game_over_time)  

    pygame.display.flip()

    clock.tick(60)

    game_time += clock.get_time()  
    if game_time > 3000:  
        obstacle_speed += 0.1  
        game_time = 0 
        obstacle_frequency += 0.5  

pygame.quit()
sys.exit()