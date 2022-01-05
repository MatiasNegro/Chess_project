import pygame_gui
import pygame

class gui:
    def main():
        pygame.init()
        manager = pygame_gui.UIManager((800, 600), './gui/theme.json')

        pygame.display.set_caption('Quick Start')
        window_surface = pygame.display.set_mode((800, 600))

        background = pygame.Surface((800, 600))
        background.fill(pygame.Color('black'))
        clock = pygame.time.Clock()
        is_running = True

        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 75), (200, 100)), text='New Game', manager=manager)
        exit_button =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 425), (200, 100)), text='Exit', manager=manager)
        options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 250), (200, 100)), text='Options', manager=manager)
        while is_running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        exec(open("./ChessMain.py").read())
                        is_running = False
                    if event.ui_element == exit_button:
                        is_running = False
                    if event.ui_element == options_button:
                        is_running = False

                        
            

                manager.process_events(event)

            manager.update(time_delta)

            window_surface.blit(background, (0, 0))
            manager.draw_ui(window_surface)

            pygame.display.update()

