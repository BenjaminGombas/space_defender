import pygame
import os

# Change the current working directory of a Python script to the directory where the script itself is
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Ship:
    """
    This class creates and manages the ship of the game

    Attributes:

    - screen :    :class:`pygame.surface.Surface` --> The screen of the game on which to draw.
    - settings :    :class:`settings.Settings` --> Game settings that control aspects of the game, such as ship speed.
    - screen_rect :    :class:`pygame.rect.Rect` --> The rect object of the screen.
    - image :    :class:`pygame.surface.Surface` --> The bitmap image of the ship character.
    - rect :    :class:`pygame.rect.Rect` --> The rect object that stores rectangular coordinates of the ship.
    - y :    :class:`float` --> The vertical position of the ship.
    - moving_up :    :class:`bool` --> Flag to determine if the ship is moving up.
    - moving_down :    :class:`bool` --> Flag to determine if the ship is moving down.

    Methods:

    - update() --> Move the ship up/down depending on the moving_up and moving_down movement flags. Returns None.
    - blitme() --> Draw the ship to the screen at its current location. Returns None.
    """

    def __init__(self, game):
        """
        Initialize the ship and set its starting position
        """
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = game.screen.get_rect()

        # Load the image and get its rect
        # Load the bitmap of the spaceship
        # Image from https://kenney.nl/assets/space-shooter-redux
        # Licensing: https://creativecommons.org/publicdomain/zero/1.0/
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'assets/images/ship2.bmp'))
        self.rect = self.image.get_rect()

        # Start each new ship at the center left of the screen
        self.rect.midleft = self.screen_rect.midleft

        # Store a decimal value for the ship's vertical position
        self.y = float(self.rect.y)

        # Movement flag
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """
        Update the ship's position based on movement flags
        :return None:
        """
        # Update the ship's x value, not the rect
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.x
        self.rect.y = self.y

    def blitme(self):
        """
        Draw the ship at its current location
        :return None:
        """
        self.screen.blit(self.image, self.rect)
