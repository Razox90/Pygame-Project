# Imports global stuff from a settings.py
from stuff import *

class Button:
    def __init__(self, x, y, width, height, text, font, font_size, text_color, button_color, hover_color, callback = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.Font(font, font_size)
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
    
    def draw(self, screen):
        # This checks whether the mouse is over the button or not.
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.button_color, self.rect)
    
        # This draws the text.
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.callback:
                        self.callback()
                    return True
        return False
    
class Main:
    def __init__(self):
        pygame.init()
        self.done = False
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
    # This is the quit function for the quit game button
    def quit_game(self):
        pygame.quit()
        sys.exit()

    # This is the start game function which starts the game whenever the start game button is pressed. 
    def start_game(self):
        from game import Game
        game = Game()
        game.run()

    # Possible wip
    def resolution_select(self):
        pass

    # This is the possible wip settings screen
    def settings_game(self):
        
        buttons = [
            Button(x = 25, y = 275, width = button_width, height = button_height, text = 'display', font = None, font_size = 36, text_color = purple, button_color = purple_1, hover_color = purple_2, callback = self.resolution_select),
            Button(x = 25, y = 375, width = button_width, height = button_height, text = 'Return', font = None, font_size = 36, text_color = purple, button_color = purple_1, hover_color = purple_2, callback = self.main_menu),
            

        ]
        
        while not self.done:
            self.screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    
                for button in buttons:
                    button.is_clicked(event)
                    
                for button in buttons:
                    button.draw(self.screen)
                  
                pygame.display.flip()

    # This is the Main menu class
    def main_menu(self):
        
        buttons = [
            Button(x = 25, y = 275, width = button_width, height = button_height, text = 'Start Game', font = None, font_size = 36, text_color = purple, button_color = purple_1, hover_color = purple_2, callback = self.start_game),
            Button(x = 25, y = 375, width = button_width, height = button_height, text = 'Settings', font = None, font_size = 36, text_color = purple, button_color = purple_1, hover_color = purple_2, callback = self.settings_game),
            Button(x = 25, y = 475, width = button_width, height = button_height, text = 'Quit Game', font = None, font_size = 36, text_color = purple, button_color = purple_1, hover_color = purple_2, callback = self.quit_game)

        ]

        while not self.done:
            # Important.
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

                for button in buttons:
                    button.is_clicked(event)

            # Draws the buttons]
            for button in buttons:
                button.draw(self.screen)

            # Refreshes the display completely.
            pygame.display.flip()
        
        # Handles quiting.
        pygame.quit()
        sys.exit()

# Starts the game.
if __name__ == "__main__":
    main = Main()
    main.main_menu()