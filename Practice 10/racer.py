import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Загрузка ресурсов
image_background = pygame.image.load('AnimatedStreet.png')
image_player = pygame.image.load('Player.png')
image_enemy = pygame.image.load('Enemy.png')
image_coin = pygame.transform.scale(pygame.image.load('coin.png'), (30, 30))

pygame.mixer.music.load('ennismore-goofy-ahh-car-horn-200870.mp3')
pygame.mixer.music.play(-1)

sound_crash = pygame.mixer.Sound('shelvis_makes_games-sus-meme-sound-181271.mp3')

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20) # Для счетчика монет

image_game_over = font.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 10
        self.generate_random_rect()

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_coin
        self.rect = self.image.get_rect()
        self.generate_random_rect()

    def generate_random_rect(self):
        max_x = WIDTH - self.rect.width
        if max_x <= 0: max_x = 370 # Защита от ошибки
        self.rect.left = random.randint(0, max_x)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, 5) 
        if self.rect.top > HEIGHT:
            self.generate_random_rect()

running = True
clock = pygame.time.Clock()
FPS = 60

# --- СОЗДАЕМ ПЕРЕМЕННЫЕ ПЕРЕД ЦИКЛОМ ---
score = 0 
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()
    
    # Проверка сбора монет
    if pygame.sprite.spritecollideany(player, coin_sprites):
        score += 1
        coin.generate_random_rect()

    screen.blit(image_background, (0, 0))

    # Движение и отрисовка всех объектов
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    # Отрисовка счета (вне условий, чтобы всегда было видно)
    score_display = font_small.render("Coins: " + str(score), True, "black")
    screen.blit(score_display, (WIDTH - 120, 10))

    # Столкновение с врагом
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)
        
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        time.sleep(3)
        running = False 
    
    pygame.display.flip() 
    clock.tick(FPS) 

pygame.quit()