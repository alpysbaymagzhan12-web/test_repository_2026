import pygame 
pygame.init()
WIGHT=500
HIGHT=500
screen=pygame.display.set_mode((WIGHT,HIGHT))
RADIUS=50
circle_x=WIGHT//2
circle_y=HIGHT//2
circle_speed=5

COLOR_RED = (255, 0, 0) 
COLOR_BLUE = (0, 0, 255)
button_up=False
button_down=False
button_right=False
button_left=False

is_red=True
run_game=True

clock = pygame.time.Clock()
FPS = 60

while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                button_up=True
            if event.key == pygame.K_DOWN:
                button_down=True
            if event.key == pygame.K_RIGHT:
                button_right=True
            if event.key == pygame.K_LEFT:
                button_left=True
            

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                button_up = False
            if event.key == pygame.K_DOWN:
                button_down = False
            if event.key == pygame.K_RIGHT:
                button_right = False
            if event.key == pygame.K_LEFT:
                button_left = False
            if circle_x - RADIUS < 0:
                circle_x = RADIUS
            if circle_x + RADIUS > WIGHT:
                circle_x = WIGHT - RADIUS
            if circle_y - RADIUS < 0:
                circle_y = RADIUS
            if circle_y + RADIUS > HIGHT:
                circle_y = HIGHT - RADIUS
            
    if button_up:
        circle_y -= circle_speed
    if button_down:
        circle_y += circle_speed
    if button_right:
        circle_x += circle_speed
    if button_left:
        circle_x -= circle_speed
    
    if is_red:
        screen.fill(COLOR_RED)
        pygame.draw.circle(screen, COLOR_BLUE, (circle_x, circle_y), 40)
    else:
        screen.fill(COLOR_BLUE)
        pygame.draw.circle(screen, COLOR_RED, (circle_x, circle_y), 40)
    pygame.display.flip() 
    clock.tick(FPS)
pygame.quit()

            