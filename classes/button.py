# !/usr/bin/env python3

"""
Created by: Mohamad Tanbari
Created on: December 2024
The button class for the Tomogotchi game.
"""

# import constants
from .. import constants
import stage
import supervisor
import ugame

# import classes
from Tomogotchi.classes.meta_sprite import Meta_Sprite


class Button(Meta_Sprite):
    """
    The main button class.
    """

    def __init__(self, x: int, y: int, style: int):
        """
        The constructor for the button class.
        
        Style:
            0 -> FEED
            1 -> PLAY
            2 -> STAT
            3 -> EXIT

        Args:
            x (int): The x position of the button.
            y (int): The y position of the button.
            Style (int): The style of the button (0 - 3).
        """

        self._x = x
        self._y = y
        self._bmp_path = ""
        self._tiles = []
        self._disabled_tiles = []
        self._style = style

        # Pick the type of button
        if self._style == 0 or self._style == 1:
            self._bmp_path = "./Tomogotchi/assets/buttons.bmp"
        elif self._style == 2 or self._style == 3:
            self._bmp_path = "./Tomogotchi/assets/buttons2.bmp"

        # Create the Button
        self._tiles = [(self._style * 4), (self._style * 4 + 1)]
        self._disabled_tiles = [(self._tiles[0] + 2), (self._tiles[1] + 2)]

        # Create the button
        super().__init__(x, y, 2, 1, self._bmp_path, self._tiles)

    # Method to press the button
    def press(self):
        """
        Press the button.
        """

        # Update sprite before trying to change its state
        for sprite in self._tile_list:
            sprite.update()

        # update the sprite to the pressed button
        self._tile_list[0].set_frame(self._disabled_tiles[0])
        self._tile_list[1].set_frame(self._disabled_tiles[1])

    # Method to release the button
    def release(self):
        """
        Release the button.
        """

        # Update sprite before trying to change its state
        for sprite in self._tile_list:
            sprite.update()

        # update the sprite to the released button
        self._tile_list[0].set_frame(self._tiles[0])
        self._tile_list[1].set_frame(self._tiles[1])
