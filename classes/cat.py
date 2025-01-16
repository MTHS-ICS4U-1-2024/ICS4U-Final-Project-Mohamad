# !/usr/bin/env python3

"""
Created by: Mohamad Tanbari
Created on: January 2025
The cat class for the Tomogotchi game.
"""

# import constants
from .. import constants
import stage
import supervisor
import ugame
import random
import json
import time
import math

# import classes
from Tomogotchi.classes.meta_sprite import Meta_Sprite

DEBUG_MODE = False


class Cat:
    """
    The cat class.
    """

    # Path to the left facing cat image
    BMP_PATH_LEFT = "./Tomogotchi/assets/left_cat.bmp"

    # Path to the right facing cat image
    BMP_PATH_RIGHT = "./Tomogotchi/assets/right_cat.bmp"

    # List of tiles to use for frame 1 of the cat
    TILES = [0, 1, 2, 3, 4, 5]

    # List of tiles to use for frame 1 of the cat flipped
    TILES_FLIPPED = [2, 1, 0, 5, 4, 3]

    # List of tiles to use for frame 2 of the cat
    TILES_ALT = [6, 7, 8, 9, 10, 11]

    # List of tiles to use for frame 2 of the cat flipped
    TILES_ALT_FLIPPED = [8, 7, 6, 11, 10, 9]

    # The farthest the cat can go left
    LEFT_BOUNDARY = 16

    # The farthest the cat can go right
    RIGHT_BOUNDARY = 146

    def __init__(self, x: int, y: int, happiness: int):
        """
        The constructor for the cat class.

        Args:
            x (int): The x position of the cat.
            y (int): The y position of the cat.
            hunger (int): The hunger level of the cat.
            happiness (int): The happiness level of the cat.
            facing (str): The direction the cat is facing ("left" or "right").
        """

        # Properties that must be filled
        self._x = x
        self._y = y
        self._happiness = happiness

        # Other properties
        self._facing = "left"
        self._walk_speed = 1
        self._frame_counter = 0
        self._tracked_frame = 0
        self._emote_duration = 1
        self._walk_distance = 0
        self._direction = 1  # 1 for right, -1 for left
        self._tile_list = []

        # Calculate new stats
        # hunger decreases at a rate of 20 every 24 hours
        # Joy decreases at a rate of 20 every 4 hours

        if not DEBUG_MODE:
            # Load json file
            with open("Tomogotchi/data.json", "r") as file:
                data = json.load(file)

                # Calculate the time since the last update
                last_checked = data["last_checked"]

                if last_checked is None:
                    last_checked = time.time()

                time_since_last_checked = time.time() - last_checked

                # Update the hunger
                data["hunger"] -= math.floor(time_since_last_checked / 86400 * 20)
                # Update the joy
                data["joy"] -= math.floor(time_since_last_checked / 14400 * 20)

                if data["hunger"] < 0:
                    data["hunger"] = 0
                if data["joy"] < 0:
                    data["joy"] = 0

                # Save the new last checked time
                data["last_checked"] = time.time()

            # Save json file
            with open("Tomogotchi/data.json", "w") as file:
                json.dump(data, file)

        # Create the cat
        self.left_side_cat = Meta_Sprite(x, y, 3, 2, Cat.BMP_PATH_LEFT, Cat.TILES)
        self.right_side_cat = Meta_Sprite(
            x, y, 3, 2, Cat.BMP_PATH_RIGHT, Cat.TILES_FLIPPED
        )

        self.right_side_cat.move_off_screen()

        # Create the emote sprite
        emote_bmp_left = stage.Bank.from_bmp16(Cat.BMP_PATH_LEFT)
        emote_bmp_right = stage.Bank.from_bmp16(Cat.BMP_PATH_RIGHT)

        self._emote_left = stage.Sprite(emote_bmp_left, 12, 255, 255)
        self._emote_right = stage.Sprite(emote_bmp_right, 12, 255, 255)

        # Track the emote sprite
        self._emote = self._emote_left

        self._tile_list = (
            [self._emote_left, self._emote_right]
            + self.left_side_cat._tile_list
            + self.right_side_cat._tile_list
        )

    # Getter for x position
    @property
    def x(self) -> int:
        """
        Get the x position of the metasprite.

        Returns:
            int: The x position of the metasprite.
        """
        return self._x

    # Setter for x position
    @x.setter
    def x(self, value: int):
        """
        Set the x position of the metasprite.

        Args:
            value (int): The new x position of the metasprite.
        """
        self._x = value

        # Update the x position of all follower sprites
        if self._facing == "left":
            self.left_side_cat.x = self._x
            if self._emote_duration > 0:
                self._emote.move(self._x - 16, self._emote.y)
        elif self._facing == "right":
            self.right_side_cat.x = self._x
            if self._emote_duration > 0:
                self._emote.move(self._x + 48, self._emote.y)

    # Getter for y position
    @property
    def y(self) -> int:
        """
        Get the y position of the metasprite.

        Returns:
            int: The y position of the metasprite.
        """
        return self._y

    # Setter for y position
    @y.setter
    def y(self, value: int):
        """
        Set the y position of the metasprite.

        Args:
            value (int): The new y position of the metasprite.
        """
        self._y = value

        # Update the y position of all follower sprites
        if self._facing == "left":
            self.left_side_cat.y = self._y
        elif self._facing == "right":
            self.right_side_cat.y = self._y

        if self._emote_duration > 0:
            self._emote.move(self._emote.x, self._y - 16)

        # getter for the joy stat

    @property
    def joy(self) -> int:
        """
        Get the joy level of the cat.

        Returns:
            int: The joy level of the cat.
        """

        # Load json file
        with open("Tomogotchi/data.json", "r") as file:
            data = json.load(file)

        return data["joy"]

    # Setter for the joy stat
    @joy.setter
    def joy(self, value: int):
        """
        Set the joy level of the cat.

        Args:
            value (int): The new joy level of the cat (0 - 100).
        """

        if not DEBUG_MODE:
            if value > 0 and value < 100:
                # Load json file
                with open("Tomogotchi/data.json", "r") as file:
                    data = json.load(file)

                data["joy"] = value

                # Save json file
                with open("Tomogotchi/data.json", "w") as file:
                    json.dump(data, file)

    @property
    # Setter for the hunger stat
    def hunger(self) -> int:
        """
        Get the hunger level of the cat.

        Returns:
            int: The hunger level of the cat.
        """

        # Load json file
        with open("Tomogotchi/data.json", "r") as file:
            data = json.load(file)

        return data["hunger"]

    @hunger.setter
    # Setter for the hunger stat
    def hunger(self, value: int):
        """
        Set the hunger level of the cat.

        Args:
            value (int): The new hunger level of the cat (0 - 100).
        """

        if not DEBUG_MODE:
            if value > 0 and value < 100:
                # Load json file
                with open("Tomogotchi/data.json", "r") as file:
                    data = json.load(file)

                data["hunger"] = value

                # Save json file
                with open("Tomogotchi/data.json", "w") as file:
                    json.dump(data, file)

    def flip(self):
        """
        Flip the cat to face the opposite direction.
        """

        # Flip the cat
        if self._facing == "left":
            self._facing = "right"
            self.right_side_cat.x = self.left_side_cat.x
            self.right_side_cat.y = self.left_side_cat.y

            # Flip the emote if it is showing
            if self._emote_duration > 0:
                # Change the sprite being used
                self._emote.move(255, 255)
                self._emote = self._emote_right
                self._emote.move(self._x + 48, self._y - 16)

            self.left_side_cat.move_off_screen()
        else:
            self._facing = "left"
            self.left_side_cat.x = self.right_side_cat.x
            self.left_side_cat.y = self.right_side_cat.y

            # Flip the emote if it is showing
            if self._emote_duration > 0:
                # Change the sprite being used
                self._emote.move(255, 255)
                self._emote = self._emote_left
                self._emote.move(self._x - 16, self._y - 16)

            self.right_side_cat.move_off_screen()

    def emote(self, emote: int, duration: int, prioritize: bool = False):
        """
        Show an emote above the cat.

        Args:
            emote (int): The emote to display (0 - 3).
            duration (int): The duration to display the emote.
        """

        if self._emote_duration == 0 or prioritize:
            # Set the emote sprite
            if self._facing == "left":
                self._emote = self._emote_left
                self._emote.move(self.x - 16, self._y - 16)
            elif self._facing == "right":
                self._emote = self._emote_right
                self._emote.move(self.x + 48, self._y - 16)

            # Change both sprite frames to the emote selected
            self._emote_left.set_frame(12 + emote)
            self._emote_right.set_frame(12 + emote)

            self._emote_duration = duration

    def react(self):
        # If hunger is low, then react with a hungry emote
        if self.hunger < 30:
            self.emote(2, 100)
        # If joy is low, then react with an angry emote
        elif self.joy < 30:
            self.emote(1, 100)
        elif self.joy > 70:
            self.emote(0, 100)

    def walk(self, direction: int, distance: int):
        """
        Walk the cat in a direction.

        Args:
            direction (int): The direction to walk the cat (0 for left or 1 for right).
            distance (int): The distance to walk the cat (in pixels).
        """
        if direction == 0:
            self._direction = -1
        else:
            self._direction = 1

        self._walk_distance = distance

    def update(self):
        """
        General method to update the cat. Most things rely on this to make the cat work.
        """

        if self._emote_duration > 0:
            self._emote_duration -= 1
            if self._emote_duration == 0:
                self._emote.move(255, 255)

        # Walking
        # Set the distance to walk
        if self._walk_distance > 0:
            # Check if the current direction the cat is facing
            #   matches the direction the cat is walking
            if self._direction == 1:
                if self._facing == "left":
                    self.flip()
            else:
                if self._facing == "right":
                    self.flip()

            # Move the cat
            self.x += self._walk_speed * self._direction

            # Check for wall collision
            if self.x <= Cat.LEFT_BOUNDARY or self.x + 48 >= Cat.RIGHT_BOUNDARY:
                self._direction *= -1
                self.flip()
                self.x += self._walk_speed * self._direction

            if self._frame_counter == 5:
                # Update the frame for the walk animation
                if self._facing == "left":
                    if self._tracked_frame == 0:
                        self.left_side_cat.swap_tiles(Cat.TILES)
                        self._tracked_frame = 1
                    else:
                        self.left_side_cat.swap_tiles(Cat.TILES_ALT)
                        self._tracked_frame = 0
                elif self._facing == "right":
                    if self._tracked_frame == 0:
                        self.right_side_cat.swap_tiles(Cat.TILES_FLIPPED)
                        self._tracked_frame = 1
                    else:
                        self.right_side_cat.swap_tiles(Cat.TILES_ALT_FLIPPED)
                        self._tracked_frame = 0

                self._frame_counter = 0
            else:
                self._frame_counter += 1

            # Update the walk distance
            self._walk_distance -= self._walk_speed

        # Randomly make the cat walk around
        if self._walk_distance == 0:
            if random.randint(1, 130) == 1:
                self.walk(random.randint(0, 1), random.randint(30, 70))

        # Randomly make the cat react
        if random.randint(1, 600) == 1:
            self.react()
