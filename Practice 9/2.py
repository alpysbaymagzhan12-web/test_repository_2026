import pygame
import math
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

background = pygame.image.load('mem.webp').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

hand_surface = pygame.Surface((150, 40), pygame.SRCALPHA)
pygame.draw.ellipse(hand_surface, (200, 150, 120), (0, 0, 150, 40))

def rotate_on_pivot(image, angle, pivot, offset):
    surf = pygame.transform.rotate(image, -angle)
    rect = surf.get_rect(center=pivot + offset.rotate(angle))
    return surf, rect

SHOULDER = pygame.Vector2(400, 300)
OFFSET = pygame.Vector2(75, 0) 
CLOCK_RADIUS = 200

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    now = datetime.now()
    angle = now.second * 6 

    screen.blit(background, (0, 0))

    pygame.draw.circle(screen, (255, 255, 255), (int(SHOULDER.x), int(SHOULDER.y)), CLOCK_RADIUS, 5)
    
    for i in range(12):
        marker_angle = math.radians(i * 30 - 90)
        start_x = SHOULDER.x + (CLOCK_RADIUS - 10) * math.cos(marker_angle)
        start_y = SHOULDER.y + (CLOCK_RADIUS - 10) * math.sin(marker_angle)
        end_x = SHOULDER.x + CLOCK_RADIUS * math.cos(marker_angle)
        end_y = SHOULDER.y + CLOCK_RADIUS * math.sin(marker_angle)
        pygame.draw.line(screen, (255, 255, 255), (start_x, start_y), (end_x, end_y), 3)

    rotated_hand, rect = rotate_on_pivot(hand_surface, angle, SHOULDER, OFFSET)
    screen.blit(rotated_hand, rect)

    pygame.draw.circle(screen, (80, 50, 30), (int(SHOULDER.x), int(SHOULDER.y)), 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()