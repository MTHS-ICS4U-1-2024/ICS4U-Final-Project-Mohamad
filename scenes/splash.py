# !/usr/bin/env python3

"""
Created by: Mohamad Tanbari
Created on: December 2024
Splash scene for the Tomogotchi game
"""

# import constants
from .. import constants
import stage
import supervisor
import ugame
import time

# Scene imports
from Tomogotchi.scenes.game import game_scene


def splash_scene():
    """
    The splash scene of the game.
    """

    try:
        # Load the image bank
        moj_corp_splash = stage.Bank.from_bmp16("./Tomogotchi/assets/moj_corp.bmp")

        # Load second image bank
        moj_corp_splash2 = stage.Bank.from_bmp16("./Tomogotchi/assets/moj_corp2.bmp")
    except Exception as e:
        print(f"Error loading image splash scene backgrounds: {e}")
        return

    background = stage.Grid(
        moj_corp_splash, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # Compacting the background tiles
    for row in range(1, 5):
        for col in range(3, 7):
            background.tile(col, row, (row - 1) * 4 + (col - 3))

    sprite = []
    sprite_positions = [(3, 5), (4, 5), (5, 5), (6, 5), (3, 6), (4, 6), (5, 6), (6, 6)]
    sprite_indices = [1, 2, 3, 4, 6, 7, 8, 9]

    for index, (x, y) in zip(sprite_indices, sprite_positions):
        bkgSprite = stage.Sprite(moj_corp_splash2, index, x * 16, y * 16)
        sprite.append(bkgSprite)

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = sprite + [background]
    game.render_block()

    while True:
        time.sleep(2.0)
        game_scene()
