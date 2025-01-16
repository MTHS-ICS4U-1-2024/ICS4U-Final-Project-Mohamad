# !/usr/bin/env python3

"""
Created by: Mohamad Tanbari
Created on: December 2024
A function to easily update a button state.
"""

# import constants
from .. import constants


def update_button_state(keys, button, key_constant):
    if keys & key_constant != 0:
        if button == constants.button_state["button_up"]:
            return constants.button_state["button_just_pressed"]
        elif button == constants.button_state["button_just_pressed"]:
            return constants.button_state["button_still_pressed"]
    else:
        if button == constants.button_state["button_still_pressed"]:
            return constants.button_state["button_released"]
        else:
            return constants.button_state["button_up"]
    return button
