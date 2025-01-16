# Tomogotchi
My final project for ICS4U

Place the code below inside of code.py after downloading this repo into the pybadge.

with open('./Tomogotchi/code.py', 'r') as file:
  code = file.read()
  exec(code)

Place the code below into boot.py

import storage

storage.remount("/", readonly=False)