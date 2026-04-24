import pygame
import random

pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 600, 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Цвета
colorWHITE, colorGRAY, colorBLACK = (255, 255, 255), (50, 50, 50), (0, 0, 0)
colorRED, colorGREEN, colorYELLOW = (255, 0, 0), (0, 255, 0), (255, 255, 0)

# Шрифты
font_info = pygame.font.SysFont("Verdana", 20)
font_game_over = pygame.font.SysFont("Verdana", 60)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx, self.dy = 1, 0
        self.dead = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # 1. ПРОВЕРКА СТОЛКНОВЕНИЯ СО СТЕНАМИ (Borders)
        if (self.body[0].x < 0 or self.body[0].x >= WIDTH // CELL or
            self.body[0].y < 0 or self.body[0].y >= HEIGHT // CELL):
            self.dead = True

        # Проверка столкновения с самим собой
        for segment in self.body[1:]:
            if self.body[0].x == segment.x and self.body[0].y == segment.y:
                self.dead = True

    def draw(self):
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            last = self.body[-1]
            self.body.append(Point(last.x, last.y))
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.pos = Point(0, 0)
        self.generate_random_pos(snake_body)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    # 2. УМНЫЙ СПАВН ЕДЫ (не на змейке)
    def generate_random_pos(self, snake_body):
        while True:
            self.pos.x = random.randint(0, (WIDTH // CELL) - 1)
            self.pos.y = random.randint(0, (HEIGHT // CELL) - 1)
            # Проверяем, не попала ли еда на сегмент змейки
            on_snake = False
            for segment in snake_body:
                if segment.x == self.pos.x and segment.y == self.pos.y:
                    on_snake = True
                    break
            if not on_snake:
                break

# Состояние игры
snake = Snake()
food = Food(snake.body)
score = 0
level = 1
FPS = 5
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1

    # Логика
    snake.move()
    
    if snake.dead:
        screen.fill(colorRED)
        msg = font_game_over.render("GAME OVER", True, colorBLACK)
        screen.blit(msg, (WIDTH // 2 - 160, HEIGHT // 2 - 30))
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    # 3 & 4. УРОВНИ И СКОРОСТЬ
    if snake.check_collision(food):
        score += 1
        food.generate_random_pos(snake.body)
        if score % 3 == 0: # Новый уровень каждые 3 еды
            level += 1
            FPS += 2

    # Отрисовка
    screen.fill(colorBLACK)
    # Сетка
    for i in range(0, WIDTH, CELL):
        for j in range(0, HEIGHT, CELL):
            pygame.draw.rect(screen, colorGRAY, (i, j, CELL, CELL), 1)

    snake.draw()
    food.draw()

    # 5. СЧЕТЧИКИ (Отрисовка в самом конце)
    s_text = font_info.render("Score: " + str(score), True, colorWHITE)
    l_text = font_info.render("Level: " + str(level), True, colorWHITE)
    screen.blit(s_text, (10, 10))
    screen.blit(l_text, (WIDTH - 110, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()