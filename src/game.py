import os
import pygame

from src.settings import *
from src.sprites import Player, Fruit, Background
from src.assets import LazyLoader, SoundManager
from src.menu import MainMenu, RankingMenu

class Game:
    # INIT
    def __init__(self):
        pygame.init()

        #SCREEN
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Snakipy")
        self.clock = pygame.time.Clock()

        self.ranking_file = os.path.join(os.path.dirname(__file__), RANKING_FILE_PATH)
        self.ranking = self.load_ranking()

        self.loader = LazyLoader()
        self.sound_manager = SoundManager()

        self.all_sprites = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()

        self.background = Background(self, [0, 0])
        self.player = Player(self, 10, 10)
        self.fruit = Fruit(self)

        self.large_font = pygame.font.SysFont("chicken_pie", 80)
        self.small_font = pygame.font.SysFont("chicken_pie", 32)

        self.score = 0
        self.font = pygame.font.SysFont("chicken_pie", 24)

        self.paused = False

        self.menu = MainMenu(self)
        self.ranking_menu = RankingMenu(self)

    # MAIN MENU
    def show_main_menu(self):
        self.menu.display()

    # RANKING
    def load_ranking(self):
        try:
            with open(self.ranking_file, "r") as file:
                scores = [int(line.strip()) for line in file.readlines()]
                return scores
        except FileNotFoundError:
            return []

    def save_ranking(self, score):
        scores = self.load_ranking()
        scores.append(score)
        scores.sort(reverse=True)
        with open(self.ranking_file, "w") as file:
            for score in scores:
                file.write(f"{score}\n")

    def update_ranking(self, new_score):
        self.ranking.append(new_score)
        self.ranking.sort(reverse=True)
        self.ranking = self.ranking[:10]  # Keep top 10 scores
        self.save_ranking(new_score)

    def display_ranking(self):
        self.ranking_menu.display()

    # RUN
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
                self.draw()
            else:
                self.draw_pause_message()
        
        self.game_over()

    # START GAME
    def start_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.background = Background(self, [0, 0])
        self.player = Player(self, 10, 10)
        self.fruit = Fruit(self)
        self.score = 0
        self.run()

    # EVENTS
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.grow()
                if event.key == pygame.K_p:
                    self.paused = not self.paused

    # UPDATE
    def update(self):
        self.all_sprites.update()

        # Check for collisions with fruits
        hits = pygame.sprite.spritecollide(
            self.player, self.fruits, False)
        for fruit in hits:
            points = FRUIT_TYPES[fruit.fruit_type]["points"]
            self.player.grow(points)
            fruit.teleport()
            # Add points based on fruit type
            self.score += points
            # Play the fruit-specific sound
            self.sound_manager.play_sound(FRUIT_TYPES[fruit.fruit_type]["sound"])

        self.playing = self.player.alive

    # PAUSE
    def draw_pause_message(self):
        pause_text = self.large_font.render("PAUSED", True, WHITE)
        self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_rect().width//2, HEIGHT // 2 - pause_text.get_rect().height//2))
        pygame.display.flip()

    # DRAW
    def draw(self):
        self.screen.fill(BGCOLOR)
        # grid

        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, DARKGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

        self.all_sprites.draw(self.screen)
        self.player.draw_body(self.screen)

        score_text = self.small_font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Nothing else to draw, let's show it!
        pygame.display.flip()

    # GAME OVER
    def game_over(self):
        title_text = self.large_font.render("GAME OVER", True, YELLOW)
        score_text = self.small_font.render(
            f"Score: {self.score} [Press any key]", True, WHITE)

        self.screen.fill(LIGHTBROWN)
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_rect().width//2, HEIGHT // 3 - title_text.get_rect().height//2))


        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_rect().width//2, HEIGHT // 2 - score_text.get_rect().height//3))

        pygame.display.flip()
        pygame.time.delay(1000)

        self.update_ranking(self.score)

        in_game_over = True

        while in_game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    in_main_menu = False
            self.start_game()



game = Game()
game.show_main_menu()
game.run()