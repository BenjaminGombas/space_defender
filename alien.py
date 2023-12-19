from random import randint
import pygame
from pygame.sprite import Sprite
import os

# Change the current working directory of a Python script to the directory where the script itself is
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Alien(Sprite):
    """
    A class to represent a single alien

    Attributes:
    - screen :    :class:`pygame.surface.Surface` --> The screen of the game on which to draw.
    - settings :    :class:`settings.Settings` --> Game settings that control aspects of the game
    - image :    :class:`tuple` --> Bitmap image of the alien
    - rect :    :class:`pygame.rect.Rect` --> The rect object that stores rectangular coordinates of the alien.
    - x :    :class:`float` --> The horizontal position of the alien.

    Methods:
    -update() --> Move the alien across the screen. Returns None.
    """

    def __init__(self, game):
        """
        Initialize the alien
        :param game:
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Load the alien image and set its rect
        # Image from https://kenney.nl/assets/space-shooter-redux
        # Licensing: https://creativecommons.org/publicdomain/zero/1.0/
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'assets/images/enemy.bmp'))
        self.rect = self.image.get_rect()

        # Start each new alien at a random position on the right side of the screen.
        self.rect.left = self.screen.get_rect().right
        # The farthest down the screen to place the alien is the height of the screen, minus the height of the alien.
        alien_top_max = self.settings.screen_height - self.rect.height
        self.rect.top = randint(0, alien_top_max)

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self, speed_factor):
        """
        Move the alien towards the left side of the screen
        :param speed_factor: a float greater than 1 that will increase the speed at which the alien moves
        :return:
        """
        self.x -= self.settings.alien_speed * speed_factor
        self.rect.x = self.x
