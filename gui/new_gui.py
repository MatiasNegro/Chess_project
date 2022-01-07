from os import WEXITED
import pygame, sys
from game import ChessMain


# Setup pygame/window ---------------------------------------- #
HEIGHT = WIDTH = 960
white = (255,255,255)
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('game base')
display_surface = pygame.display.set_mode((HEIGHT, WIDTH))
font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 50)
text = font.render('UNIBCHESS', True, (0,0,0))
display_surface.fill((255,255,255))
display_surface.blit(text, (330, 117))
click = False
 
def main_menu():
    while True:

        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(330, 311, 300, 75)
        button_2 = pygame.Rect(330, 416, 300, 75)
        button_3 = pygame.Rect(330, 521, 300, 75)

        text_1 = button_font.render('SINGLEPLAYER', True, white)
        text_2 = button_font.render('MULTIPLAYER', True, white)
        text_3 = button_font.render('EXIT', True, white)
        

        if button_1.collidepoint((mx, my)):
            if click:
                ChessMain.main()
                
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        
        
        pygame.draw.rect(display_surface, (0, 0, 0), button_1)
        pygame.draw.rect(display_surface, (0, 0, 0), button_2)
        pygame.draw.rect(display_surface, (0, 0, 0), button_3)
        display_surface.blit(text_1, (350, 331))
        display_surface.blit(text_2, (350, 436))
        display_surface.blit(text_3, (430, 541))
 
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)
 
