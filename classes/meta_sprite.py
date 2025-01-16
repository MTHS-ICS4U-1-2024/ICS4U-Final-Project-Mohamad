# !/usr/bin/env python3

"""
Created by: Mohamad Tanbari
Created on: December 2024
The meta sprite class for the Tomogotchi game.
"""

# import constants
from .. import constants
import stage
import supervisor
import ugame


class Meta_Sprite:
    """
    Create meta sprites for the game.
    """

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        sprite_sheet_position: str,
        tiles: list,
    ):
        """
        The constructor for the meta_sprite class.

        Args:
            x (int): The x position of the sprite.
            y (int): The y position of the sprite.
            sprite_sheet_position (str): The position of the sprite in the sprite sheet.
        """

        self._x = x
        self._y = y
        self._height = height
        self._width = width
        self._tile_list = []
        self._tiles = tiles
        self._sprite_sheet_position = sprite_sheet_position

        # Load the image bank
        try:
            self.image_bank = stage.Bank.from_bmp16(self._sprite_sheet_position)
        except Exception as e:
            print(f"Error loading image sprite: {e}")
            return

        # Loop to create sprites for each tile entered
        for index, tile in enumerate(self._tiles):
            # Calculate the x and y position of the tile
            meta_sprite_x = (index % self._width) * constants.SPRITE_SIZE
            meta_sprite_y = (index // self._width) * constants.SPRITE_SIZE
            self.sprite = stage.Sprite(
                self.image_bank, tile, self.x + meta_sprite_x, self.y + meta_sprite_y
            )

            # Add the sprite to the tile list
            self._tile_list.append(self.sprite)

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
        for index, sprite in enumerate(self._tile_list):
            # Calculate the x and y position of the tile
            meta_sprite_x = (index % self._width) * constants.SPRITE_SIZE
            sprite.move(self._x + meta_sprite_x, sprite.y)

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
        for index, sprite in enumerate(self._tile_list):
            # Calculate the x and y position of the tile
            meta_sprite_y = (index // self._width) * 16
            sprite.move(sprite.x, self._y + meta_sprite_y)

    # Method to move the metasprite off screen
    def move_off_screen(self):
        """
        Move the metasprite off screen.
        """

        self.x = constants.OFF_SCREEN_X
        self.y = constants.OFF_SCREEN_Y

    # Method to change the tiles of the metasprite
    def swap_tiles(self, tiles: list):
        """
        Swap the tiles of the metasprite.

        Args:
            tiles (list): The new tiles for the metasprite.
        """

        # Update the tiles
        self._tiles = tiles

        # Loop to update the tiles
        for index, tile in enumerate(self._tiles):
            self._tile_list[index].set_frame(tile)

    # Method to check if the sprite is on screen
    def is_on_screen(self) -> bool:
        """
        Check if the sprite is on screen.

        Returns:
            bool: Whether the sprite is on screen or not.
        """

        return self.x != constants.OFF_SCREEN_X and self.y != constants.OFF_SCREEN_Y
