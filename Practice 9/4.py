import pygame

pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Music Player")


background = pygame.image.load('WhatsApp Image 2026-04-17 at 23.56.29.JPEG').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


songs = [
    "Rick Astley — Never Gonna Give You Up (www.lightaudio.ru).mp3",
    "Ерболат Құдайбергенов - MEN QAZAQPYN.mp3",
    "song3.mp3"
]
current_song_index = 0


pygame.mixer.music.load(songs[current_song_index])
pygame.mixer.music.play(-1)

run = True
while run:
    
    screen.blit(background, (0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_p:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            
            if event.key == pygame.K_s:
                pygame.mixer.music.stop()
            
        
            if event.key == pygame.K_r:
                pygame.mixer.music.play(-1)
            
            
            if event.key == pygame.K_q:
                run = False

            if event.key == pygame.K_n:
                current_song_index = (current_song_index + 1) % len(songs)
                pygame.mixer.music.load(songs[current_song_index])
                pygame.mixer.music.play(-1)
                print(f"Сейчас играет: {songs[current_song_index]}")

            
            if event.key == pygame.K_b:
                current_song_index = (current_song_index - 1) % len(songs)
                pygame.mixer.music.load(songs[current_song_index])
                pygame.mixer.music.play(-1)
                print(f"Сейчас играет: {songs[current_song_index]}")

    
    pygame.display.flip()

pygame.quit()