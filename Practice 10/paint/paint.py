import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((0, 0, 0)) # Заполним черным, чтобы ластик стирал до фона

colorRED = (255, 0, 0)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)

clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

currX = 0
currY = 0
prevX = 0
prevY = 0

# Режимы: 'rect', 'circle', 'eraser'
mode = 'rect' 

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Выбор режима клавишами
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_e: mode = 'eraser'
            
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1
            if event.key == pygame.K_MINUS:
                THICKNESS = max(1, THICKNESS - 1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX, prevY = event.pos

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX, currY = event.pos
                screen.blit(base_layer, (0, 0)) # Очищаем экран перед предпросмотром
                
                if mode == 'rect':
                    pygame.draw.rect(screen, colorRED, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
                elif mode == 'circle':
                    # Вычисляем радиус как расстояние от центра до текущей мыши
                    radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
                    pygame.draw.circle(screen, colorRED, (prevX, prevY), radius, THICKNESS)
                elif mode == 'eraser':
                    # Ластик рисует прямо на базовом слое черным цветом
                    pygame.draw.circle(base_layer, colorBLACK, (currX, currY), THICKNESS * 2)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            
            # Рисуем финальную фигуру на базовом слое
            if mode == 'rect':
                pygame.draw.rect(base_layer, colorRED, calculate_rect(prevX, prevY, currX, currY), THICKNESS)
            elif mode == 'circle':
                radius = int(((prevX - currX)**2 + (prevY - currY)**2)**0.5)
                pygame.draw.circle(base_layer, colorRED, (prevX, prevY), radius, THICKNESS)
            
            screen.blit(base_layer, (0, 0))

    # Если мы ничего не рисуем в данный момент, просто показываем базу
    if not LMBpressed:
        screen.blit(base_layer, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()