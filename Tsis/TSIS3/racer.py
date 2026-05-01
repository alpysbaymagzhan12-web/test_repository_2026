import pygame
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_img(name, w, h):
    path = os.path.join(BASE_DIR, name)
    if not os.path.exists(path):
        path = os.path.join(BASE_DIR, "assets", name)
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (w, h))
    return img

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = get_img("car.png", 45, 90)
        self.rect = self.image.get_rect(center=(200, 520))
        self.mask = pygame.mask.from_surface(self.image)
        self.shield = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.move_ip(-7, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < 400: self.rect.move_ip(7, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = get_img("enemy.png", 45, 90)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(50, 350), -100)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > 600: self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = get_img("coin.png", 30, 30)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(50, 350), -50)

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > 600: self.reset()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, kind):
        super().__init__()
        self.kind = kind # "nitro" или "shield"
        self.image = pygame.Surface((30, 30))
        # Нитро - красный, Щит - синий
        self.image.fill((255, 0, 0) if kind == "nitro" else (0, 0, 255))
        self.rect = self.image.get_rect(center=(random.randint(50, 350), -200))

    def move(self):
        self.rect.move_ip(0, 4)