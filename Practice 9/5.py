import pygame
import math
from datetime import datetime

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")
clock = pygame.time.Clock()


background = pygame.image.load('mickeyclock.jpeg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


def draw_hand(angle, length, width, color):
    
    radians = math.radians(angle - 90)
    

    end_x = CENTER[0] + length * math.cos(radians)
    end_y = CENTER[1] + length * math.sin(radians)
    
    pygame.draw.line(screen, color, CENTER, (end_x, end_y), width)

CENTER = (WIDTH // 2, HEIGHT // 2)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.now()
    
    sec_angle = now.second * 6
    min_angle = now.minute * 6 + now.second * 0.1
    hour_angle = (now.hour % 12) * 30 + (now.minute * 0.5)

    screen.blit(background, (0, 0))

    draw_hand(hour_angle, 140, 10, (0, 0, 0)) 

    draw_hand(min_angle, 190, 7, (0, 0, 0))
    
    draw_hand(sec_angle, 210, 3, (200, 0, 0))

    pygame.draw.circle(screen, (0, 0, 0), CENTER, 12)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()