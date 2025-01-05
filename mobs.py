"""
This contains anything that moves within the game.
Anything that does not move is stored elsewhere 

List of mobs:
Fairy : The generic term for our workers, as narrativly they are little fairies.
TestFairy : A member of the Fairy class used for testing

"""

import pygame
import random
from user_settings import *

class Fairy(pygame.sprite.Sprite):
    def __init__(self, x, y, color=(127, 127, 127)):  # Default to grey if no color is provided
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)  # Use the passed color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class TestFairy(Fairy):  # TestFairy is a subclass of fairy
    def __init__(self, x = None, y = None):
        #Make a random color
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Generate random x and y within the screen bounds
        if x == None:
            x = random.randint(200, SCREEN_WIDTH - 10)  # Subtracting the fairy's size (10x10)
        if y == None:
            y = random.randint(0, SCREEN_HEIGHT - 10)  # Subtracting the fairy's size (10x10)

        super().__init__(x, y, color=random_color)
        self.special_attribute = "Test"
