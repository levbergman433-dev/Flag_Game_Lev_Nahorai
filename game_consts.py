import pygame
import random
import math
import sys
import Screen
import game_field
import soldier
import state

pygame.init()

GRID_ROWS = 25
GRID_COLS = 50
CELL_SIZE = 25

WIDTH = GRID_COLS * CELL_SIZE
HEIGHT = GRID_ROWS * CELL_SIZE
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))

# PLAYER SIZE IN GRID UNITS
PLAYER_ROWS = 4
PLAYER_COLS = 2


clock = pygame.time.Clock()

COLOR_WALL = (40, 40, 50)
COLOR_EMPTY = (0,0,0,0)
COLOR_PLAYER = (255, 215, 0)
COLOR_DIAMOND = (0, 195, 255)
COLOR_MINE = (230, 50, 50)
COLOR_TEXT = (255, 255, 255)
# color of the background !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
COLOR_PANEL = (0, 98, 18)

TILE_EMPTY = 0
TILE_GRASS = 1
TILE_DIAMOND = 2
TILE_MINE = 3

# running states
RUNNING_STATE = 0
state = {}
HINT_STATE = 1
LOST_STATE = 2
WIN_STATE = 3



