import pygame_gui
import pygame

class gui:
    def main():
        pygame.init()
        manager = pygame_gui.UIManager((960,960))

        pygame.display.set_caption('Quick Start')
        window_surface = pygame.display.set_mode((960, 960))

        background = pygame.Surface((960, 960))
        background.fill(pygame.Color('black'))
        clock = pygame.time.Clock()
        is_running = True
        game_path = "game\ChessMain.py"


        title_text_box = pygame_gui.elements.UILabel(relative_rect=pygame.rect(330,280,400,75), text="UNIBCHESS", manager=manager)
        hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 311), (300, 75)), text='SINGLEPLAYER', manager=manager)
        exit_button =  pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 341), (300, 75)), text='MULTIPLAYER', manager=manager)
        options_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((280, 371), (300, 75)), text='EXIT', manager=manager)
        while is_running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == hello_button:
                        exec(open("game/ChessMain.py").read())
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

    if __name__ == "__main__":
        main()