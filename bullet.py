import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """
    A class to manage bullets fired from the ship

    Attributes:

    - screen :    :class:`pygame.surface.Surface` --> The screen of the game on which to draw.
    - settings :    :class:`settings.Settings` --> Game settings that control aspects of the game, such as bullet speed, color, and size.
    - color :    :class:`tuple` --> The RGB color value of the bullet.
    - rect :    :class:`pygame.rect.Rect` --> The rect object that stores rectangular coordinates of the bullet.
    - x :    :class:`float` --> The horizontal position of the bullet.

    Methods:

    - update() --> Move the bullet across the screen. Returns None.
    - draw_bullet() --> Draw the bullet to the screen. Returns None.
    """

    def __init__(self, game):
        """
        Create a new Bullet object at the ship's position
        :param game:
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0,0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # Align the left side of the bullet with the right side of the ship
        self.rect.midleft = game.ship.rect.midright

        # Store the bullet's position as a decimal value
        self.x = float(self.rect.x)

    def update(self):
        """
        Move the bullet up the screen
        :return None:
        """
        # Update the decimal place position of the bullet
        self.x += self.settings.bullet_speed
        # Update the rect position
        self.rect.x = self.x

    def draw_bullet(self):
        """
        Draw the bullet to the screen
        :return None:
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
