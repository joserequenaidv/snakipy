import pygame
import random

from src.settings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, game, location):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # Create background surface
        try:
            self.image = game.loader.get_image(IMAGE_BACKGROUND)
        except FileNotFoundError:
            self.image = pygame.Surface((WIDTH, HEIGHT))
            self.image.fill((20, 20, 20))  # Dark black background
                
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.direction = "right"
        
        # Player head image
        try:
            self.image = game.loader.get_image(PLAYER_HEADIMAGE[self.direction]["image"])
        except FileNotFoundError:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.fill(BLACK)
        
        self.rect = self.image.get_rect()
        
        # Player body image
        try:
            self.body_image = game.loader.get_image(PLAYER_BODYIMAGE[self.direction]["image"])
        except FileNotFoundError:
            self.body_image = pygame.Surface((TILESIZE, TILESIZE))
            self.body_image.fill(WHITE)
        
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.speed = 10
        self.turn = 0
        self.body = []  
        self.body_length = 1  
        self.alive = True

    def update_body(self):
        # Add current position to the body
        self.body.insert(0, (self.x, self.y))
        # Keep the body length consistent
        if len(self.body) > self.body_length:
            self.body.pop()

    def draw_body(self, screen):
        for segment in self.body:
            screen.blit(self.body_image, (segment[0] * TILESIZE, segment[1] * TILESIZE))

    def grow(self, amount=1):
        self.body_length += amount 

    def update(self):
        self.move()
        self.wrap_around_world()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def move(self):
        self.turn += self.speed * self.game.dt
        
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT] and self.dx == 0:
            self.dx = -1
            self.dy = 0
            self.direction = "left"
            self.image = self.game.loader.get_image(PLAYER_HEADIMAGE[self.direction]["image"])
            self.body_image = self.game.loader.get_image(PLAYER_NECKIMAGE[self.direction]["image"])
        if keystate[pygame.K_RIGHT] and self.dx == 0:
            self.dx = 1
            self.dy = 0
            self.direction = "right"
            self.image = self.game.loader.get_image(PLAYER_HEADIMAGE[self.direction]["image"])
            self.body_image = self.game.loader.get_image(PLAYER_NECKIMAGE[self.direction]["image"])
        if keystate[pygame.K_UP] and self.dy == 0:
            self.dy = -1
            self.dx = 0
            self.direction = "up"
            self.image = self.game.loader.get_image(PLAYER_HEADIMAGE[self.direction]["image"])
            self.body_image = self.game.loader.get_image(PLAYER_NECKIMAGE[self.direction]["image"])
        if keystate[pygame.K_DOWN] and self.dy == 0:
            self.dy = 1
            self.dx = 0
            self.direction = "down"
            self.image = self.game.loader.get_image(PLAYER_HEADIMAGE[self.direction]["image"])
            self.body_image = self.game.loader.get_image(PLAYER_NECKIMAGE[self.direction]["image"])

        if (self.turn >= 1):
            self.turn = 0
            self.update_body()
            self.x += self.dx
            self.y += self.dy
            self.check_death()

    def wrap_around_world(self):
        # Wrap horizontally
        if self.x >= GRIDWIDTH:
            self.x = 0
        if self.x < 0:
            self.x = GRIDWIDTH - 1
        
        # Wrap vertically
        if self.y >= GRIDHEIGHT:
            self.y = 0
        if self.y < 0:
            self.y = GRIDHEIGHT - 1

    def update_body(self):
        if len(self.body) > self.body_length:
            self.body.pop()
        self.body.insert(0, (self.x, self.y))


    def draw_body(self, surface):
        for i in range(0, len(self.body)):
            x = self.body[i][0] * TILESIZE
            y = self.body[i][1] * TILESIZE
            surface.blit(self.body_image, (x, y))

    def check_death(self):
        is_stopped = self.dx != 0 or self.dy != 0
        if is_stopped and (self.x, self.y) in self.body:
            self.alive = False
            print("OUCH!")

class Fruit(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = game.all_sprites, game.fruits
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.set_random_fruit()
        self.teleport()

    def set_random_fruit(self):
        self.fruit_type = random.choice(list(FRUIT_TYPES.keys()))
        try:
            self.image = self.game.loader.get_image(FRUIT_TYPES[self.fruit_type]["image"])
        except FileNotFoundError:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.fill(RED)
        self.rect = self.image.get_rect()

    def teleport(self):
        # Get all possible grid positions
        possible_positions = set((x,y) for x in range(GRIDWIDTH) for y in range(GRIDHEIGHT))
        
        # Get snake occupied positions (body and head)
        snake_positions = set(self.game.player.body)
        snake_positions.add((self.game.player.x, self.game.player.y))
        
        # Calculate available positions
        available_positions = possible_positions - snake_positions
        
        # If no positions available, end game - victory
        if not available_positions:
            print("You've won!")
            self.game.playing = False
            return

        # Divide grid into quadrants
        quadrant_width = GRIDWIDTH // 2
        quadrant_height = GRIDHEIGHT // 2
        
        # Get snake's current quadrant
        snake_quadrant_x = self.game.player.x // quadrant_width
        snake_quadrant_y = self.game.player.y // quadrant_height

        # Get positions in opposite quadrant
        opposite_quadrant_positions = {
            (x,y) for (x,y) in available_positions 
            if (x // quadrant_width) != snake_quadrant_x 
            and (y // quadrant_height) != snake_quadrant_y
        }

        # Choose position (prefer opposite quadrant if available)
        if opposite_quadrant_positions:
            x, y = random.choice(list(opposite_quadrant_positions))
        else:
            x, y = random.choice(list(available_positions))

        self.set_random_fruit()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
