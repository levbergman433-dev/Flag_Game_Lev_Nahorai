import pygame
import random
import math
import sys

pygame.init()

GRID_ROWS = 25
GRID_COLS = 50
CELL_SIZE = 20
WIDTH = GRID_COLS * CELL_SIZE
HEIGHT = GRID_ROWS * CELL_SIZE

# PLAYER SIZE IN GRID UNITS
PLAYER_ROWS = 4
PLAYER_COLS = 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

COLOR_WALL = (40, 40, 50)
COLOR_EMPTY = (0,0,0,0)
COLOR_PLAYER = (255, 215, 0)
COLOR_DIAMOND = (0, 195, 255)
COLOR_MINE = (230, 50, 50)
COLOR_TEXT = (255, 255, 255)
# color of the background !!!
# COLOR_PANEL = (0, 98, 18)
COLOR_PANEL = (0,0,0)

TILE_EMPTY = 0
TILE_WALL = 1
TILE_DIAMOND = 2
TILE_MINE = 3


def generate_random_dungeon(rows, cols):
    grid = []
    count_mine = 0
    for r in range(rows):
        row = []
        count_per_row = 0
        for c in range(cols):
            # FIXED BUG 5: border on the bottom row (rows - 1)
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                row.append(TILE_EMPTY)
            else:
                rand_val = random.randint(0, 100)
                if rand_val >= 99 and rand_val <= 100:
                    iswall = True
                else:
                    iswall = False

                if iswall == True and count_mine == 20:
                    iswall = False
                if count_per_row >= 3:
                    iswall = False
                if iswall == True and c >= cols - 3:
                    iswall = False

                if iswall == True:
                    #grid overflow when laying out mines
                    count_mine += 1
                    count_per_row += 1
                    mines_to_add = 3
                    for i in range(mines_to_add):
                        row.append(TILE_MINE)
                    c = c + (mines_to_add - 1)
                else:
                    row.append(TILE_EMPTY)
        grid.append(row)
    # clear an area of PLAYER_ROWS x PLAYER_COLS starting at (1,1) so player doesn't spawn stuck
    for pr in range(1, 1 + PLAYER_ROWS):
        for pc in range(1, 1 + PLAYER_COLS):
            if pr < rows - 1 and pc < cols - 1:
                grid[pr][pc] = TILE_EMPTY
    # put diamonds in the end
    for r in range(rows - 3, rows):
        for c in range(cols - 4, cols):
            grid[r][c] = TILE_DIAMOND

    return grid


def calculate_distance(r1, c1, r2, c2):
    # FIXED: Replaced faulty calculation math formula with the proper Pythagorean distance
    dist = math.sqrt((r1 - r2) ** 2 + (c1 - c2) ** 2)
    return dist


def find_nearest_diamond(grid, player_r, player_c):
    min_dist = 999999
    nearest_pos = None

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == TILE_DIAMOND:
                d = calculate_distance(player_r, player_c, r, c)
                if d < min_dist:
                    min_dist = d
                    nearest_pos = (r, c)

    return nearest_pos, min_dist


def move_player(grid, player_r, player_c, dr, dc):
    new_r = player_r + dr
    new_c = player_c + dc

    # check every cell covered by the new 6x2 footprint
    for pr in range(PLAYER_ROWS):
        for pc in range(PLAYER_COLS):
            check_r = new_r + pr
            check_c = new_c + pc
            grid_len = len(grid)
            grid_0_len = len(grid[0])
            # out of bounds check or hitting a wall
            if check_r >= len(grid) or check_c >= len(grid[0]) or grid[check_r][check_c] == TILE_WALL:
                return player_r, player_c, 0, False

    collected_score = 0
    hit_mine = False
    did_hit_diamond = False
    # process items within the new footprint space
    for pr in range(PLAYER_ROWS):
        for pc in range(PLAYER_COLS):
            target_r = new_r + pr
            target_c = new_c + pc

            if grid[target_r][target_c] == TILE_DIAMOND:
                did_hit_diamond = True
                grid[target_r][target_c] = TILE_EMPTY
            elif grid[new_r + 3][target_c] == TILE_MINE:
                hit_mine = True
                grid[target_r][target_c] = TILE_EMPTY

    return new_r, new_c, did_hit_diamond, hit_mine


# def count_remaining_diamonds(grid):
#     count = 0
#     for row in grid:
#         for cell in row:
#             if cell == TILE_DIAMOND:
#                 count += 1
#     return count


def main():
    dungeon = generate_random_dungeon(GRID_ROWS, GRID_COLS)
    player_r, player_c = 1, 1
    did_hit_diamond = False
    lives = 1
    level = 1

    font = pygame.font.SysFont("Arial", 20)

    running = True
    while running:
        screen.fill(COLOR_PANEL)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                dr, dc = 0, 0
                if event.key == pygame.K_UP:
                    dr = -1
                elif event.key == pygame.K_DOWN:
                    dr = 1
                elif event.key == pygame.K_LEFT:
                    dc = -1
                elif event.key == pygame.K_RIGHT:
                    dc = 1

                if dr != 0 or dc != 0:
                    player_r, player_c, did_hit_diamond, mine = move_player(dungeon, player_r, player_c, dr, dc)
                    if mine:
                        lives -= 1
                        print("BOOM! Hit a mine. Lives left:", lives)

        # remaining = count_remaining_diamonds(dungeon)
        if did_hit_diamond:
            did_hit_diamond = False
            level += 1
            print(f"Level {level} Complete! Generating new dungeon...")
            dungeon = generate_random_dungeon(GRID_ROWS, GRID_COLS)
            player_r, player_c = 1, 1

        # draw the grid tiles
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                rect_x = c * CELL_SIZE
                rect_y = r * CELL_SIZE

                tile_type = dungeon[r][c]
                # color = (COLOR_PANEL)
                color = ((0,0,0))
                if tile_type == TILE_WALL:
                    color = COLOR_WALL
                elif tile_type == TILE_DIAMOND:
                    color = COLOR_DIAMOND
                elif tile_type == TILE_MINE:
                    color = COLOR_MINE

                pygame.draw.rect(screen, color, (rect_x, rect_y, CELL_SIZE - 2, CELL_SIZE - 2))

        # DRAW LARGE PLAYER: Scale width by PLAYER_COLS (2) and height by PLAYER_ROWS (6)
        player_x = player_c * CELL_SIZE + 4
        player_y = player_r * CELL_SIZE + 4
        player_width = (CELL_SIZE * PLAYER_COLS) - 8
        player_height = (CELL_SIZE * PLAYER_ROWS) - 8
        pygame.draw.rect(screen, COLOR_PLAYER, (player_x, player_y, player_width, player_height))


        if lives <= 0:
            print("GAME OVER!")
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
