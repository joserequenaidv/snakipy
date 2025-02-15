import pygame
import random

from settings import *

class Background(pygame.sprite.Sprite):
    def __init__(self, game, location):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        # Create background surface
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((20, 20, 20))  # Dark black background
        
        # Create vintage pattern
        for x in range(0, WIDTH, 20):
            for y in range(0, HEIGHT, 20):
                pygame.draw.circle(self.image, (40, 40, 40), (x, y), 2)
                
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.tail_image = pygame.Surface((TILESIZE, TILESIZE))
        self.tail_image.fill(WHITE)
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.speed = 10
        self.turn = 0
        self.tail = []
        self.tail_length = 1
        self.alive = True

    def grow(self):
        self.tail_length += 1

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
        if keystate[pygame.K_RIGHT] and self.dx == 0:
            self.dx = 1
            self.dy = 0
        if keystate[pygame.K_UP] and self.dy == 0:
            self.dy = -1
            self.dx = 0
        if keystate[pygame.K_DOWN] and self.dy == 0:
            self.dy = 1
            self.dx = 0

        if (self.turn >= 1):
            self.turn = 0
            self.update_tail()
            self.x += self.dx
            self.y += self.dy
            self.check_death()

    def wrap_around_world(self):
        if self.x > GRIDWIDTH:
            self.x = 0
        if self.x > GRIDWIDTH-1:
            self.x = 0
        if self.x > GRIDHEIGHT:
            self.x = 0
        if self.y > GRIDHEIGHT-1:
            self.y = 0

    def update_tail(self):
        if len(self.tail) > self.tail_length:
            self.tail.pop()
        self.tail.insert(0, (self.x, self.y))


    def draw_tail(self, surface):
        for i in range(0, len(self.tail)):
            x = self.tail[i][0] * TILESIZE
            y = self.tail[i][1] * TILESIZE
            surface.blit(self.tail_image, (x, y))

    def check_death(self):
        is_stopped = self.dx != 0 or self.dy != 0
        if is_stopped and (self.x, self.y) in self.tail:
            self.alive = False
            print("OUCH!")

class Fruit(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.groups = game.all_sprites, game.fruits
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.teleport()

    def teleport(self):
        # Get all possible grid positions
        possible_positions = set((x,y) for x in range(GRIDWIDTH) for y in range(GRIDHEIGHT))
        
        # Get snake occupied positions (body and head)
        snake_positions = set(self.game.player.tail)
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

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
