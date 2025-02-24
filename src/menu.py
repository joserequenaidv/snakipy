import pygame
from src.settings import *

class Menu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.selected_option = 0
    
    def draw_option(self, text, position, selected=False):
        color = SELECTED_COLOR_MENU if selected else UNSELECTED_COLOR_MENU
        font = pygame.font.SysFont(OPTION_TEXT_FONT_TYPE, OPTION_TEXT_FONT_SIZE)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, position))
        self.screen.blit(text_surface, text_rect)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                return self.handle_keydown(event.key)
        return False

class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.options = MENU_OPTIONS
    
    def handle_keydown(self, key):
        if key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif key == pygame.K_RETURN:
            if self.selected_option == 0:
                self.game.start_game()
                return True
            elif self.selected_option == 2:
                self.game.display_ranking()
                return True
        return False
    
    def display(self):
        while True:
            self.screen.fill(MAIN_MENU_BG)
            
            for i, option in enumerate(self.options):
                self.draw_option(
                    option, 
                    HEIGHT // 5 + i * 80,
                    i == self.selected_option
                )
            
            pygame.display.flip()
            
            if self.handle_input():
                break

class RankingMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_keydown(self, key):
        if key == pygame.K_RETURN:
            return True
        return False
        
    def display(self):
        while True:
            self.screen.fill(MAIN_MENU_BG)
            
            # Dibujar título
            title_font = pygame.font.SysFont(RANKING_TITLE_FONT_TYPE, RANKING_TITLE_FONT_SIZE)
            title_text = title_font.render("RANKING", True, RANKING_TITLE_COLOR)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 30))
            self.screen.blit(title_text, title_rect)
            
            # Dibujar puntuaciones
            for i, score in enumerate(self.game.ranking[:10]):
                score_text = f"{i + 1}. {score}"
                self.draw_option(score_text, 100 + i * 40)
            
            # Dibujar texto de retorno
            self.draw_option("Press ENTER to return", HEIGHT - 50)
            
            pygame.display.flip()
            
            if self.handle_input():
                break 