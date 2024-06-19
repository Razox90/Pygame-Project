import pygame, sys, os
from os.path import join
from pytmx.util_pygame import load_pygame
from PIL import Image

screen_width = 1280
screen_height = 720

# Button color
purple = (44, 22, 74)
purple_1 = (55, 52, 87)
purple_2 = (67, 63, 105)

button_width = screen_width / 6
button_height = screen_height / 8


# game.py

TILE_SIZE = 16
