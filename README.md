# Tomogotchi
This is my final project for ICS4U. It is a simplified version of the Tomogotchi, built to run on the pybadge!

## Setup
1. Download the entire repository into the PyBadge.
11. If the repository name is not "Tomogotchi" you must rename it.
2. Create a file called `code.py` in the root directory of the PyBadge.
3. Place the following code inside `code.py`:
    ```python
    with open('./Tomogotchi/code.py', 'r') as file:
        code = file.read()
        exec(code)
    ```
4. Create a file called `boot.py` in the root directory of the PyBadge.
5. Place the following code inside `boot.py`:
    ```python
    import storage
    storage.remount("/", readonly=False)
    ```
6. Unplug the pybadge and restart it by powering it off and on.

## What is this game?
You want to keep your cat happy. Keep its hunger and joy meters from reaching zero! Your cat's happiness and hunger will go down over time, so make sure to check on it frequently.

## How do I play this game?
- Press the buttons corresponding to the icons shown on screen to interact with your pet!
- Pressing `FEED` will create a burger that the cat will eat. This action increases your cat's hunger meter.
- Pressing the `PLAY` button will create a tennis ball for your cat to play with. This action will increase the cat's joy meter.
- Holding the `STAT` button will show you the cat's hunger and joy.