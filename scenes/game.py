# !/usr/bin/env python3

"""
Created by: Mohamad Tanbari
Created on: December 2024
Splash game/menu scene for the Tomogotchi game
"""

# Import constants
from .. import constants
import stage
import supervisor
import ugame
import time
import random

# Import classes
from ..classes.meta_sprite import Meta_Sprite
from ..classes.button import Button
from ..classes.cat import Cat

# Import utils
from ..utils.update_button_state import update_button_state


def game_scene():
    """
    The game scene of the game.
    """

    try:
        # load image banks
        background_bank = stage.Bank.from_bmp16(
            "./Tomogotchi/assets/game_scene_background.bmp"
        )
        test_bank = stage.Bank.from_bmp16("./Tomogotchi/assets/buttons.bmp")
    except Exception as e:
        print(f"Error loading image banks: {e}")
        return

    tile_map = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 2],
        [3, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 4, 4, 4, 4, 4, 4, 4, 4, 5],
        [3, 7, 7, 7, 7, 7, 7, 7, 7, 5],
        [3, 6, 6, 6, 6, 6, 6, 6, 6, 5],
        [3, 4, 4, 6, 4, 4, 6, 4, 4, 5],
        [8, 9, 9, 9, 9, 9, 9, 9, 9, 10],
    ]

    background = stage.Grid(
        background_bank, constants.SCREEN_GRID_X, constants.SCREEN_GRID_Y
    )

    # Fill background using tile map
    for row in range(0, 8):
        for col in range(0, 10):
            background.tile(col, row, tile_map[row][col])

    # Initialize buttons
    down = constants.button_state["button_up"]
    up = constants.button_state["button_up"]
    left = constants.button_state["button_up"]
    right = constants.button_state["button_up"]

    feed_button = Button(16, (6 * 16), 0)
    play_button = Button((16 * 4), (6 * 16), 1)
    stat_button = Button((16 * 7), (6 * 16), 2)

    button_sprites = (
        stat_button._tile_list + play_button._tile_list + feed_button._tile_list
    )

    # Initialize the cat
    cat = Cat(56, 16 * 3, 0)

    # Initialize the text
    text = []
    hunger = stage.Text(
        width=29,
        height=14,
    )
    hunger.move(255, 255)
    hunger.text("Hunger: " + str(cat.hunger) + "/100")
    text.append(hunger)

    joy = stage.Text(
        width=29,
        height=14,
    )
    joy.move(255, 255)
    joy.text("Joy: " + str(cat.joy) + "/100")
    text.append(joy)

    # Create food and toy
    extras_bank = stage.Bank.from_bmp16("./Tomogotchi/assets/extras.bmp")
    food = stage.Sprite(extras_bank, 0, 255, 255)
    toy = stage.Sprite(extras_bank, 1, 255, 255)

    # Variables to track the toy
    toy_counter = 0
    toy_velocity_x = 0
    toy_velocity_y = 0

    game = stage.Stage(ugame.display, constants.FPS)
    game.layers = text + cat._tile_list + [food, toy] + button_sprites + [background]
    game.render_block()

    # Game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        # Track button data
        right = update_button_state(keys, right, ugame.K_RIGHT)
        left = update_button_state(keys, left, ugame.K_LEFT)
        down = update_button_state(keys, down, ugame.K_DOWN)

        # Testing
        up = update_button_state(keys, up, ugame.K_UP)

        # Button functionality
        if left == constants.button_state["button_just_pressed"]:
            feed_button.press()

            random_x = random.randint(cat.LEFT_BOUNDARY, cat.RIGHT_BOUNDARY - 16)

            # Ensure food doesn't appear inside the cat
            while (
                cat.x < random_x + 16
                and cat.x + 48 > random_x
                and cat.y < 16 * 4 + 16
                and cat.y + 32 > 16 * 4
            ):
                random_x = random.randint(cat.LEFT_BOUNDARY, cat.RIGHT_BOUNDARY - 16)

            # move the food sprite away from the cat but still on screen
            food.move(random_x, 16 * 4)
        elif left == constants.button_state["button_released"]:
            feed_button.release()

        if down == constants.button_state["button_just_pressed"]:
            play_button.press()

            random_x = random.randint(cat.LEFT_BOUNDARY, cat.RIGHT_BOUNDARY - 16)

            # Ensure food doesn't appear inside the cat
            while (
                cat.x < random_x + 16
                and cat.x + 48 > random_x
                and cat.y < 16 * 4 + 16
                and cat.y + 32 > 16 * 4
            ):
                random_x = random.randint(cat.LEFT_BOUNDARY, cat.RIGHT_BOUNDARY - 16)

            # move the food sprite away from the cat but still on screen
            toy.move(random_x, 16 * 4)

            if toy_counter < 0:
                toy_counter = 0
                cat.joy += 30
        elif down == constants.button_state["button_released"]:
            play_button.release()

        if right == constants.button_state["button_just_pressed"]:
            stat_button.press()

            # Update the text
            hunger.clear()
            joy.clear()
            hunger.cursor(0, 0)
            joy.cursor(0, 0)
            hunger.text("Hunger: " + str(cat.hunger) + "/100")
            joy.text("Joy: " + str(cat.joy) + "/100")

            joy.move(16, 28)
            hunger.move(16, 16)
            game.render_block(1, 1)
        elif right == constants.button_state["button_released"]:
            stat_button.release()

            joy.move(255, 255)
            hunger.move(255, 255)
            game.render_block()

        # Check collision between cat and food
        if (
            cat.x < food.x + 16
            and cat.x + 48 > food.x
            and cat.y < food.y + 16
            and cat.y + 32 > food.y
        ):
            cat.hunger += 10
            food.move(255, 255)
            cat.emote(3, 150, True)

        # Check collision between cat and toy
        if (
            cat.x < toy.x + 16
            and cat.x + 48 > toy.x
            and cat.y < toy.y
            and cat.y + 32 > toy.y
        ):
            cat.joy += 10

            if cat._facing == "left":
                toy_velocity_x = -1
                toy_velocity_y = -1
            elif cat._facing == "right":
                toy_velocity_x = 1
                toy_velocity_y = -1

        # Toy bouncing
        # Only if it is on screen
        if toy.x != 255:
            # Apply gravity
            toy_velocity_y += constants.GRAVITY

            # Move the toy
            toy.move(toy.x + toy_velocity_x, toy.y + toy_velocity_y)

            # Check for boundaries and bounce
            if toy.y < 16:
                toy_velocity_y = abs(toy_velocity_y) * constants.FRICTION
            elif toy.y > 64:
                toy.y = 64  # Reset position to floor level
                toy_velocity_y = -abs(toy_velocity_y) * constants.FRICTION

            if toy.x < 16:
                toy.x = 16
                toy_velocity_x = abs(toy_velocity_x) * constants.FRICTION
            elif toy.x > 130:
                toy.x = 130
                toy_velocity_x = -abs(toy_velocity_x) * constants.FRICTION

            # Apply friction to gradually stop the toy
            toy_velocity_x *= constants.FRICTION
            toy_velocity_y *= constants.FRICTION

            # Stop bouncing after velocity is very low
            if abs(toy_velocity_x) < 0.1 and abs(toy_velocity_y) < 0.1:
                toy_velocity_x = 0
                toy_velocity_y = 0

        if toy_counter == 1500:
            toy.move(255, 255)
            toy_counter = 0

        toy_counter += 1

        # specific updates
        cat.update()

        game.render_sprites(button_sprites + cat._tile_list + [food, toy])
        game.tick()
