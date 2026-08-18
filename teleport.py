import pygame
import game_consts
from Screen import draw_image
from game_consts import *
import time


pit_location = []

def exit_pit():
    hole_outside = random.choice(pit_location)
    return hole_outside






"""


import pygame
import game_consts
from Screen import draw_image
from game_consts import *
import time



pit_location = []



def draw_pit(dungeon):
    # draw pit
    for r2 in range(game_consts.GRID_ROWS):
        c = 0
        while c < game_consts.GRID_COLS:
            tile_type = dungeon[r2][c]
            if tile_type == game_consts.TILE_PIT:
                rect_x = (c + 1) * game_consts.CELL_SIZE
                rect_y = r2 * game_consts.CELL_SIZE
                draw_image('pit', rect_x, rect_y, 3 * game_consts.CELL_SIZE, 2 * game_consts.CELL_SIZE)
                c += 3
            else:
                c += 1
   """