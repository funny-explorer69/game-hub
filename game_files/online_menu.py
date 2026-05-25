import pygame
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from game_files.screen import display

class online_menu(display):
    def __init__(self):
        self.clock = pygame.time.Clock()
        super().__init__()
        pygame.display.set_caption("online menu")
    def start_online_menu(self):
        a = pygame.Rect(440,40,400,200)
        b = pygame.Rect(440,260,400,200)
        c = pygame.Rect(440,480,400,200)
        while True:
            self.screen.fill((255,255,255))
            pygame.draw.rect(self.screen,(0,0,0),a)
            pygame.draw.rect(self.screen,(0,0,0),b)
            pygame.draw.rect(self.screen,(0,0,0),c)
            surface = pygame.Surface((a.width,a.height),pygame.SRCALPHA)
            pos = pygame.mouse.get_pos()
            surface.fill((255,255,255,120))
            if a.collidepoint(pos):
                self.screen.blit(surface,a.topleft)
            elif b.collidepoint(pos):
                self.screen.blit(surface,b.topleft)
            elif c.collidepoint(pos):
                self.screen.blit(surface,c.topleft)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if i.type == pygame.MOUSEBUTTONDOWN:
                    if a.collidepoint(pos):
                        pass
                    elif b.collidepoint(pos):
                        pass
                    elif c.collidepoint(pos):
                        return False
            pygame.display.update()
            self.clock.tick(60)