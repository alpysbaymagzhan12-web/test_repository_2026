import pygame

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.SysFont("Verdana", 20)

    def draw(self, sc):
        pygame.draw.rect(sc, (220, 220, 220), self.rect)
        pygame.draw.rect(sc, (0, 0, 0), self.rect, 2)
        txt = self.font.render(self.text, True, (0,0,0))
        sc.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_txt(sc, text, size, x, y, color=(0,0,0)):
    font = pygame.font.SysFont("Verdana", size)
    txt = font.render(text, True, color)
    sc.blit(txt, txt.get_rect(center=(x, y)))