import pygame
import sys
import random
from racer import Player, Enemy, Coin, PowerUp, get_img
from persistence import update_leaderboard, load_json
from ui import Button, draw_txt

pygame.init()
SC = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Mega Racer 2026")
CLOCK = pygame.time.Clock()

def game_loop(name):
    # Инициализация переменных
    base_speed = 5
    score = 0
    distance = 0
    nitro_timer = 0
    
    player = Player()
    enemies = pygame.sprite.Group(Enemy(base_speed))
    coins = pygame.sprite.Group(Coin())
    powerups = pygame.sprite.Group()
    road = get_img("road.png", 400, 600)

    # Экран готовности
    ready = False
    while not ready:
        SC.blit(road, (0,0))
        draw_txt(SC, f"Привет, {name}!", 30, 200, 250, (255,255,255))
        draw_txt(SC, "Нажми любую клавишу", 20, 200, 300, (255,255,255))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]: ready = True

    # Главный цикл игры
    running = True
    while running:
        SC.blit(road, (0,0))
        distance += 1
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

        player.move()
        
        # Сложность: увеличиваем базовую скорость каждые 1000 метров
        if distance % 1000 == 0:
            base_speed += 1

        # Появление бонусов
        if random.randint(1, 800) == 1:
            powerups.add(PowerUp(random.choice(["nitro", "shield"])))

        # Логика Нитро
        current_enemy_speed = base_speed + 5 if nitro_timer > 0 else base_speed
        if nitro_timer > 0: nitro_timer -= 1

        # Обновление и отрисовка
        for e in enemies: 
            e.speed = current_enemy_speed
            e.move()
            SC.blit(e.image, e.rect)
        for c in coins: 
            c.move()
            SC.blit(c.image, c.rect)
        for p in powerups: 
            p.move()
            SC.blit(p.image, p.rect)
        
        SC.blit(player.image, player.rect)

        # Сбор монет
        if pygame.sprite.spritecollideany(player, coins):
            score += 10
            for c in coins: c.reset()
        
        # Подбор бонусов
        for p in pygame.sprite.spritecollide(player, powerups, True):
            if p.kind == "nitro": nitro_timer = 180 # 3 секунды
            if p.kind == "shield": player.shield = True

        # Столкновения с врагами (по маске)
        if pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_mask):
            if player.shield:
                player.shield = False
                for e in enemies: e.reset()
            else:
                update_leaderboard(name, score)
                running = False 

        # UI в игре
        draw_txt(SC, f"Счет: {score}", 20, 60, 30, (0,0,0))
        draw_txt(SC, f"Км: {distance//100}", 20, 60, 60, (0,0,0))
        if player.shield: draw_txt(SC, "ЩИТ", 20, 350, 30, (0,0,255))
        if nitro_timer > 0: draw_txt(SC, "НИТРО!", 20, 340, 60, (255,0,0))
        
        pygame.display.update()
        CLOCK.tick(60)

def show_leaders():
    while True:
        SC.fill((245, 245, 245))
        draw_txt(SC, "РЕКОРДЫ", 35, 200, 60)
        data = load_json("leaderboard.json", [])
        for i, res in enumerate(data):
            draw_txt(SC, f"{i+1}. {res['name']} - {res['score']}", 22, 200, 130 + i*35)
        
        btn_back = Button("НАЗАД", 125, 500, 150, 50)
        btn_back.draw(SC)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and btn_back.clicked(e.pos): return
        pygame.display.update()

def main_menu():
    b1 = Button("ИГРАТЬ", 100, 220, 200, 50)
    b2 = Button("ЛИДЕРЫ", 100, 290, 200, 50)
    b3 = Button("ВЫХОД", 100, 360, 200, 50)
    while True:
        SC.fill((255, 255, 255))
        draw_txt(SC, "MEGA RACER", 45, 200, 120)
        for b in [b1, b2, b3]: b.draw(SC)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if b1.clicked(e.pos):
                    u = input("Введите ваше имя: ")
                    game_loop(u if u.strip() else "Player")
                if b2.clicked(e.pos): show_leaders()
                if b3.clicked(e.pos): pygame.quit(); sys.exit()
        pygame.display.update()

if __name__ == "__main__":
    main_menu()