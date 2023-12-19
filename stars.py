import os
from random import randint

import pygame
from pygame.sprite import Sprite


class Stars(Sprite):
    """
    A class to represent a star.

    Attributes:

    - star :    :class:`pygame.surface.Surface` --> Stores a bitmap image of a star
    - small_meteor :    :class:`pygame.surface.Surface` --> Stores a bitmap image of a small meteor
    - medium_meteor :    :class:`pygame.surface.Surface` --> Stores a bitmap image of a medium meteor
    - image :    :class:`pygame.surface.Surface` --> Stores a bitmap image of a star/meteor
    - rect :    :class:`pygame.rect.Rect` --> The rect object that stores rectangular coordinates of the star/meteor

    Methods:

    - update() --> Move the stars/meteors across the screen and redraw them at the right when they go off-screen.
    Returns None.
    """

    def __init__(self, x, y, random_num):
        """
        Initialize a Star/meteor
        :param x: The x coordinate the star or meteor will be located at
        :param y: The y coordinate the star or meteor will be located at
        :param random_num: A random int between 0-100
        """
        # Call the constructor of the inherited Sprite class
        super().__init__()
        # Load the image of the star and meteors
        # Image from https://kenney.nl/assets/space-shooter-redux
        # Licensing: https://creativecommons.org/publicdomain/zero/1.0/
        self.star = pygame.image.load(os.path.join(os.getcwd(), 'assets/images/star.bmp'))
        self.small_meteor = pygame.image.load(os.path.join(os.getcwd(), 'assets/images/meteor_small.bmp'))
        self.medium_meteor = pygame.image.load(os.path.join(os.getcwd(), 'assets/images/meteor_medium.bmp'))

        # 80% chance for a star
        if random_num >= 20:
            self.image = self.star
        # 10% chance for a medium meteor
        elif random_num >= 10:
            self.image = self.medium_meteor
        # 10% chance for a small meteor
        else:
            self.image = self.small_meteor

        # Store the rect of the image and set its position based on the x,y passed to the constructor
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        """
        Move the stars and meteors across the screen and redraw them at the right when they go off-screen
        :return None:
        """
        self.rect.x -= .51
        # When a star or meteor goes off the screen, redraw it somewhere between 25 pixels away from the side of the
        # screen and the side of the screen. These two values gave me the best results for creating a constant flow of
        # drop.
        if self.rect.x < 0:
            self.rect.x = randint(1280, 1305)