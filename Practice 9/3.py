import pygame
import math
from datetime import datetime


pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)

CENTER = (WIDTH // 2, HEIGHT // 2)
RADIUS = 250

def draw_hand(angle, length, width, color):
   
    radians = math.radians(angle - 90)
    
    x = CENTER[0] + length * math.cos(radians)
    y = CENTER[1] + length * math.sin(radians)
    
    pygame.draw.line(screen, color, CENTER, (x, y), width)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.now()
    second = now.second
    minute = now.minute
    hour = now.hour % 12  

  
    screen.fill(WHITE)

    pygame.draw.circle(screen, BLACK, CENTER, RADIUS, 4)
    for i in range(12):
        angle = i * 30
        rad = math.radians(angle - 90)
        x = CENTER[0] + (RADIUS - 20) * math.cos(rad)
        y = CENTER[1] + (RADIUS - 20) * math.sin(rad)
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 5)

    
    sec_angle = second * 6
   
    min_angle = minute * 6 + second * 0.1
   
    hour_angle = hour * 30 + minute * 0.5


    draw_hand(hour_angle, RADIUS * 0.5, 8, BLACK)   
    draw_hand(min_angle, RADIUS * 0.8, 5, BLACK)    
    draw_hand(sec_angle, RADIUS * 0.9, 2, RED)      

    pygame.draw.circle(screen, BLACK, CENTER, 8)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()