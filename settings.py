class Settings:
    """
    This class stores all settings for the game.

    Attributes:

    - screen_width :    :class:`int` --> The width of the screen in pixels.
    - screen_height :    :class:`int` --> The height of the screen in pixels.
    - screen_bg_color :    :class:`tuple` --> The RGB color value of the background of the screen.
    - ship_speed :    :class:`float` --> How much to move the ship character per update call.
    - bullet_speed :    :class:`float` --> How much to move the bullet per update call.
    - bullet_width :    :class:`int` --> The width of each bullet.
    - bullet_height :    :class:`int` --> The height of each bullet.
    - bullet_color :    :class:`tuple` --> The RGB color value of each bullet.
    - bullets_allowed :    :class:`int` --> The number of bullets allowed on the screen at any given time.
    - alien_frequency :    :class:`float` --> A number to control how often aliens are generated.
    - alien_speed :    :class:`float` --> How fast to move an alien across the screen per update call.
    - alien_speed_factor :    :class:`float` --> A multiplier to cause the aliens to move more quickly.
    - lives :    :class:`int` --> The number of extra lives the player has before the game ends.
    - score :    :class:`int` --> The number of aliens the player has shot and destroyed.
    """

    def __init__(self):
        """
        Initialize the game's settings
        """
        # Screen settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (24, 41, 60)

        # Ship settings
        self.ship_speed = 3.0

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 3

        # Alien settings.
        self.alien_frequency = 0.004
        self.alien_speed = 1.5
        self.alien_speed_factor = 1.0

        # Game controls
        self.lives = 3
        self.score = 0
