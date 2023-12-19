#!/usr/bin/env python
# Davenport University
# Class Info: CISP253-23151 (Fall 2023)
# Author:     Benjamin Gombas
# Contact:    bgombas@email.davenport.edu
# Program name: gombas-w12_SidewaysShooter
"""
Creates a game that begins with a ship on the left side of the screen. The player is then able to use the up and down
arrow keys to move the ship up and down. By pressing the space bar, the player is able to fire bullets from the ship.
Only 3 bullets can be fired/on the screen at a time. Aliens are randomly generated and move towards the left side of the
screen. Hitting an alien with a bullet will destroy the alien. If an alien hits the ship or the left side of the screen,
the player loses a life. When 3 lives has been lost, the game will end. The game keeps track of the player's highest score.
"""

# Libraries to be imported
import os
import sys
import pygame

from ship import Ship
from stars import Stars
from alien import Alien
from bullet import Bullet
from random import random, randint
from settings import Settings

# Change the current working directory of a Python script to the directory where the script itself is
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# Classes
class Game:
    """
    Overall class to control and manage game assets and behaviors.

    Attributes:

    - aliens :    :class:`pygame.sprite.Group` --> The group of alien sprites
    - bullets :    :class:`pygame.sprite.Group` --> The group of bullet sprites
    - clock :    :class:`pygame.time.Clock` --> The clock object to help track time
    - font :    :class:`pygame.font.Font` --> The font used to write game over
    - game_over :    :class:`bool` --> A boolean to indicate if the game state should stop
    - lives :    :class:`int` --> The number of lives the player has before the game ends
    - lives_images :    :class:`list` --> A list of images to indicate how many lives the player has left
    - screen :    :class:`pygame.surface.Surface` --> The game screen
    - settings :    :class:`settings.Settings` --> An instance of Settings that will control the game
    - ship :    :class:`ship.Ship` --> An instance of Ship

    Methods:

    - _init_game_assets() --> Initialize/store the main game assets, such as settings, fonts, sounds, etc.
    - _draw_background() --> Create a grid of stars and meteors to give a space vibe. For each cell of the grid, there will be 18% chance of generating a star/meteor. Upon creating the meteor/star, it will be added to the stars sprite group :return None:
    - run_game() --> Start the main loop for the game
    - _display_lives() --> For each image in lives_images, display them in the top left
    - _read_high_score() --> Read high_score.txt to access the stored highest score. If no file is found, set the high score to 0
    - _write_high_score() --> Write the highest score to the highscore file
    - _display_high_score() --> Display the highest score on the screen
    - _display_score() --> Display the score on the screen
    - _check_events() --> Respond to key presses and mouse events
    - _check_keydown_events() --> Respond to keypresses :param event: The event that was triggered
    - _check_keyup_events() --> Respond to key releases :param event: The event that was triggered
    - _fire_bullet() --> Create a new bullet and add it to the bullets group
    - _update_bullets() --> Update the position of bullets and get rid of old bullets
    - _check_collision() --> Check to see if a bullet collides with an alien. If they do collide, remove both sprites from their groups
    - _create_alien() --> Create an alien instance and add it the game's alien sprite group
    - _update_aliens() --> Update the position of the aliens and check for collisions
    - _check_collision_left() --> For each of the aliens on the screen, check the horizontal position to see if any aliens have collided with the left side of the screen.
    - _lose_life() --> Decrease the number of remaining lives, display an X in place of the life indicator, and - if no lives remain - set the game_over flag to True.
    - _game_over() --> Render text on the screen to indicate the game has ended.
    - _draw_play_button() --> Draw the play button on the screen
    - _check_play_button() --> Check to see if the play button has been clicked :param mouse_pos: The position of the mouse cursor
    - _restart_game_state() --> Restart the game state to the initial state
    - _fresh_screen() --> Draw the elements that will be drawn on each new screen
    - _update_screen() --> Update images on the screen and flip to the new screen
    """

    def __init__(self):
        """
        Initialize the game and create game resources
        """
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Alien Defense")

        # Initialize game assets
        self._init_game_assets()

        # Read in the high score from high_score.txt
        self._read_high_score()

        # Flags to indicate the game state
        # game_over indicates that a game has ended
        self.game_over = False
        # game_started indicates that no game has been played since the program was run
        self.game_started = False

    def _init_game_assets(self):
        """
        Initialize/store the main game assets, such as settings, fonts, sounds, etc.
        :return None:
        """
        # Store the clock
        self.clock = pygame.time.Clock()

        # Draw the game's background
        self._draw_background()

        # Store game settings
        self.settings = Settings()
        self.lives = self.settings.lives
        self.score = self.settings.score
        self.alien_speed_factor = self.settings.alien_speed_factor
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # Store the fonts used for displaying text
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # Initialize the play button
        self.play_button = pygame.Rect((1280 / 2) - 50, 720 / 2, 100, 50)

        # Initialize the game's Ship, bullet group, and alien group
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Store the sounds used in the game
        # Sounds from https://kenney.nl/assets/space-shooter-redux
        # Licensing: https://creativecommons.org/publicdomain/zero/1.0/
        self.shoot_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'assets/sfx/sfx_laser1.ogg'))
        self.alien_hit_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'assets/sfx/sfx_zap.ogg'))
        self.ship_hit_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'assets/sfx/sfx_twoTone.ogg'))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'assets/sfx/sfx_lose.ogg'))
        # Music by https://pixabay.com/users/alexiaction-26977400/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=171561
        pygame.mixer.music.load(os.path.join(os.getcwd(), 'assets/sfx/music.mp3'))
        # Cut the volume of the music
        pygame.mixer.music.set_volume(0.1)

    def _draw_background(self):
        """
        Create a grid of stars and meteors to give a space vibe. For each cell of the grid, there will be 18% chance of
        generating a star/meteor. Upon creating the meteor/star, it will be added to the stars sprite group
        :return None:
        """
        # Create a sprite group to store the meteors/stars
        self.stars = pygame.sprite.Group()
        grid_rows = 720 // 50
        # Determine the number of columns by using modulus to get the number of raindrops that can fit across the screen
        grid_cols = 1280 // 50
        # Create a grid of raindrops
        for row in range(grid_rows):
            for col in range(grid_cols):
                # Determine if a star or meteor should be generated
                star_chance = randint(0, 100)
                # 18% chance of creating a star
                if star_chance >= 82:
                    # Determine the x,y coordinates to place the star at by multiplying by which row and column the
                    # loop is on. randint provides a bit of randomness to give a more realistic look.
                    x = col * (1280 // grid_cols) + randint(-20, 20)
                    y = row * (720 // grid_rows) + randint(-20, 20)
                    # Create a star/meteor at the above x,y coordinates
                    star = Stars(x, y, randint(0, 100))
                    # Add the star to the sprite group
                    self.stars.add(star)

    def run_game(self):
        """
        Start the main loop for the game
        :return None:
        """
        while True:
            self._check_events()
            if not self.game_over and self.game_started:
                self._display_lives()
                self._create_alien()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(240)

    def _display_lives(self):
        """
        For each image in lives_images, display them in the top left
        :return None:
        """
        if self.lives == 3:
            # Image from https://kenney.nl/assets/space-shooter-redux
            # Licensing: https://creativecommons.org/publicdomain/zero/1.0/
            life_image = os.path.join(os.getcwd(), 'assets/images/life.bmp')
            # TODO: Turn into _draw_lives but inline for loop is fine for now
            self.lives_images = [pygame.image.load(life_image) for _ in range(3)]
        # For each life image, blit it to the screen in the top left
        for i, image in enumerate(self.lives_images):
            x = i * 40
            y = 10
            self.screen.blit(image, (x, y))

    def _read_high_score(self):
        """
        Read high_score.txt to access the stored highest score. If no file is found, set the high score to 0
        :return None:
        """
        try:
            file_path = os.path.join(os.getcwd(), "assets/high_score.txt")
            with open(file_path, 'r') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

    def _write_high_score(self):
        """
        Write the highest score to the highscore file
        :return None:
        """
        file_path = os.path.join(os.getcwd(), "assets/high_score.txt")
        with open(file_path, 'w') as file:
            file.write(str(self.high_score))

    def _display_high_score(self):
        """
        Display the highest score on the screen
        :return:
        """
        # TODO: I should really refactor this so it's not basically the same chunk of code 4 times
        # If the game has been started and a game is actively being played, display the highest score in the top right
        if not self.game_over and self.game_started:
            # WOOOOO ternary killing readability
            # If the highest score is higher than the current score, display the highest score. If the current score is
            # higher than the highest score, display the current score as the highest score
            high_score_text = self.small_font.render(
                f"High Score: {self.high_score if self.high_score > self.score else self.score}", True, (0, 0, 0))
            # Move the text to the top right
            high_score_rect = high_score_text.get_rect(topleft=(self.settings.screen_width - 200, 35))
            # Blit the text to the screen
            self.screen.blit(high_score_text, high_score_rect)
        else:
            # If the game is in the "select play button" state, display the highest score in middle of the screen
            # slightly above the play button
            high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
            # Move the text to the appropriate spot
            high_score_rect = high_score_text.get_rect(center=(1280 // 2, 720 // 2 - 50))
            # Blit the text to the screen
            self.screen.blit(high_score_text, high_score_rect)

    def _display_score(self):
        """
        Display the score on the screen
        :return None:
        """
        # If a round of the game is currently being played, display the score in the top right
        if not self.game_over and self.game_started:
            score_text = self.small_font.render(f"Score: {self.score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(topleft=(self.settings.screen_width - 200, 10))
            self.screen.blit(score_text, score_rect)
        # If the round has ended, display the score in the middle of the screen
        elif self.game_over:
            score_text = self.small_font.render(f"Score: {self.score}", True, (0, 0, 0))
            score_rect = score_text.get_rect(center=(1280 // 2, 720 // 2 - 25))
            self.screen.blit(score_text, score_rect)

    def _check_events(self):
        """
        Respond to key presses and mouse events
        :return None:
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """
        Respond to keypresses
        :param event: The event that was triggered
        :return None:
        """
        # Only respond to arrow key and space presses when the game is not over but a game has been started
        if event.key == pygame.K_UP and (not self.game_over and self.game_started):
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN and (not self.game_over and self.game_started):
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE and (not self.game_over and self.game_started):
            self._fire_bullet()
        elif event.key == pygame.K_p:
            if self.game_over or not self.game_started:
                self._restart_game_state()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """
        Respond to key releases
        :param event: The event that was triggered
        :return None:
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """
        Create a new bullet and add it to the bullets group
        :return None:
        """
        # Only allow 3 bullets to be on the screen
        if len(self.bullets) < self.settings.bullets_allowed:
            # If there are fewer than 3 bullets on the screen, create a new bullet
            new_bullet = Bullet(self)
            # Add the new bullet to the bullet group
            self.bullets.add(new_bullet)
            self.shoot_sound.play()

    def _update_bullets(self):
        """
        Update the position of bullets and get rid of old bullets
        :return None:
        """
        # Update the bullets position
        self.bullets.update()

        # Get rid of bullets that have gone off of the screen
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                # Remove the bullet from the group
                self.bullets.remove(bullet)

        # Check to see if the bullet collides with an alien. Part of 13-5
        self._check_collision()

    # _check_collision is part of 13-5
    def _check_collision(self):
        """
        Check to see if a bullet collides with an alien. If they do collide, remove both sprites from their groups
        :return None:
        """
        bullet_alien_collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if bullet_alien_collisions:
            self.score += 1
            self.alien_hit_sound.play()
            # Increase the alien speed based on the score of the player
            if self.score % 5 == 0 and self.score != 0:
                self.alien_speed_factor += .1

    # _create_alien is part of 13-5
    def _create_alien(self):
        """
        Create an alien instance and add it the game's alien sprite group
        :return None:
        """
        # Use RNG to determine if an alien should be created in order to give a more random pacing to the creation
        if random() < self.settings.alien_frequency:
            alien = Alien(self)
            # Add the alien to the sprite group
            self.aliens.add(alien)

    # _update_aliens is part of 13-5
    def _update_aliens(self):
        """
        Update the position of the aliens and check for collisions
        :return None:
        """

        # Move the aliens across the screen
        self.aliens.update(self.alien_speed_factor)

        # If the ship sprite rect collides with any of the alien sprites, remove the sprite and call _lose_life()
        if pygame.sprite.spritecollide(self.ship, self.aliens, True):
            self._lose_life()

        # Look for aliens that have hit the left edge of the screen.
        self._check_collision_left()

    # _check_collision_left() is a part of 13-6
    def _check_collision_left(self):
        """
        For each of the aliens on the screen, check the horizontal position to see if any aliens have collided with the
        left side of the screen.
        :return:
        """
        for alien in self.aliens:
            if alien.rect.x < 0:
                # If the alien has hit the left side of the screen, remove the alien sprite from the group
                self.aliens.remove(alien)
                # If the alien has hit the left side of the screen, call _lose_life()
                self._lose_life()

    # _lose_life is part of 13-6
    def _lose_life(self):
        """
        Decrease the number of remaining lives, display an X in place of the life indicator, and - if no lives remain -
        set the game_over flag to True.
        :return None:
        """
        # Subtract a life from the
        self.lives -= 1
        self.ship_hit_sound.play()
        # Image from https://kenney.nl/assets/space-shooter-redux
        # Licensing: https://creativecommons.org/publicdomain/zero/1.0/
        lost_life_image = os.path.join(os.getcwd(), 'assets/images/x.bmp')
        # Replace the lost life image with a new image if lives remain
        self.lives_images[self.lives] = pygame.image.load(lost_life_image)
        if self.lives == 0:
            self.game_over_sound.play()
            self._game_over()

    # _game_over() is part of 13-6
    def _game_over(self):
        """
        Render text on the screen to indicate the game has ended.
        :return None:
        """
        # Stop the music
        pygame.mixer.music.stop()

        # If the score is higher than the highest score
        if self.score > self.high_score:
            # Set the highest score equal to the score
            self.high_score = self.score
            # Write the high score to the text file
            self._write_high_score()
        # Flip to a fresh screen
        self._fresh_screen()
        # Display the high score
        self._display_high_score()

        self.game_over = True
        text = self.font.render("Game Over", True, (0, 0, 0))
        # Move the text to the middle of the screen
        text_rect = text.get_rect(center=(1280 // 2, 720 // 2 - 100))
        # Draw the text to the screen
        self.screen.blit(text, text_rect)

    def _draw_play_button(self):
        """
        Draw the play button on the screen
        :return None:
        """
        # Draw a rectangle to represent the button
        pygame.draw.rect(self.screen, (248, 52, 43), self.play_button)
        # Draw text for the play button
        play_button_text = self.small_font.render("Play", True, (255, 255, 255))
        # Place the text on the button
        play_button_text_rect = play_button_text.get_rect(
            center=self.play_button.center
        )
        # Blit the button to the screen
        self.screen.blit(play_button_text, play_button_text_rect)

    def _check_play_button(self, mouse_pos):
        """
        Check to see if the play button has been clicked
        :param mouse_pos: The position of the mouse cursor
        :return:
        """
        if self.play_button.collidepoint(mouse_pos):
            self._restart_game_state()

    def _restart_game_state(self):
        """
        Restart the game state to the initial state
        :return None:
        """
        self.game_over = False
        self.game_started = True
        self.aliens.empty()
        self.bullets.empty()
        self.lives = self.settings.lives
        self.score = 0
        self.alien_speed_factor = 1.0
        # Play the music on a loop
        pygame.mixer.music.play(-1)

    def _fresh_screen(self):
        """
        Draw the elements that will be drawn on each new screen
        :return None:
        """
        # Draw the ship to the screen
        self.ship.blitme()
        # Draw the images that represent lives to the screen
        self._display_lives()

        self._display_score()
        self._display_high_score()

    def _update_screen(self):
        """
        Update images on the screen and flip to the new screen
        :return None:
        """
        # Fill the screen with the background color
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        # Redraw the screen during each pass though the loop
        if not self.game_over and self.game_started:
            self._fresh_screen()
            self.stars.update()
            # Draw all the bullets in the sprite group
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            # Aliens are a part of 13-5
            # Draw the aliens
            self.aliens.draw(self.screen)
        # Ending the game is part of 13-6
        # If the game over flag is set to true, end the game
        elif self.game_over:
            self._game_over()
            self._draw_play_button()
        # If the game has just been opened and a round has not been played
        elif not self.game_over and not self.game_started:
            self._draw_play_button()
            self._display_high_score()
        # Make the most recently drawn screen visible
        pygame.display.flip()


# Program Starts Here
# main()
def main():
    """
    Create an instance of the Game class and call the run_game() method
    """
    Game().run_game()


# ===============================
# No extra Code beyond this point
if __name__ == '__main__':
    main()
# EOF #
