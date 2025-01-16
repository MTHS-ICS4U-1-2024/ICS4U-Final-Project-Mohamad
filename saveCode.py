# !/usr/bin/env python3

# This script moves everything inside of there into the Tomogotchi folder inside of the PyBadge
# Done to conserve space on the PyBadge and to speed up github actions

# Copy everything in this directory aside from restricted files to the PyBadge

import os
import shutil


def copy_to_circuitpy(src, dst):
    # Ensure the destination directory exists
    if not os.path.exists(dst):
        os.makedirs(dst)

    # Get the list of files and directories in the source directory
    src_items = set(os.listdir(src))

    # Get the list of files and directories in the destination directory
    dst_items = set(os.listdir(dst))

    # Copy new and updated files from src to dst
    for item in src_items:
        if (
            item.startswith(".git")
            or item.startswith(".vscode")
            or item.startswith("saveCode")
            or item.startswith("design")
        ):
            continue
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            shutil.copy2(src_path, dst_path)

    # Remove files and directories in dst that are not in src
    for item in dst_items - src_items:
        dst_path = os.path.join(dst, item)
        if os.path.isdir(dst_path):
            shutil.rmtree(dst_path)
        else:
            os.remove(dst_path)


if __name__ == "__main__":
    src_directory = os.getcwd()
    dst_directory = "/Volumes/CIRCUITPY/Tomogotchi"
    try:
        copy_to_circuitpy(src_directory, dst_directory)
    except error:
        print(error)
