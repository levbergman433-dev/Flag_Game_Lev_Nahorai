import game_consts
from game_consts import *




def generate_random_dungeon(rows, cols):
    # create a blank grid first using simple for loops
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(game_consts.TILE_EMPTY)
        grid.append(row)

    count_mine = 0
    mines_to_add = 3

    # run your random generation logic safely by modifying grid[r][c]
    for r in range(rows):
        count_per_row = 0
        c = 0
        while c < cols:
            # enforce emptiness on sides
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                grid[r][c] = game_consts.TILE_EMPTY
                c += 1
            else:
                rand_val = random.randint(30, 100)
                iswall = False
                if rand_val >= 99 and rand_val <= 100:
                    iswall = True

                if iswall and count_mine >= 20:
                    iswall = False
                if count_per_row >= 3:
                    iswall = False
                if iswall and c >= cols - 4:
                    iswall = False
                if iswall == True:
                    for i in range(mines_to_add):
                        if c + i < cols - 1:
                            if grid[r - 1][c + i] == game_consts.TILE_MINE:
                                iswall = False
                if iswall:
                    count_mine += 1
                    count_per_row += 1
                    for i in range(mines_to_add):
                        if c + i < cols - 1:
                            grid[r][c + i] = game_consts.TILE_MINE
                    c = c + mines_to_add
                else:
                    grid[r][c] = game_consts.TILE_EMPTY
                    c += 1

    # clear player spawn area
    for pr in range(1, 1 + game_consts.PLAYER_ROWS):
        for pc in range(1, 1 + game_consts.PLAYER_COLS):
            if pr < rows - 1 and pc < cols - 1:
                grid[pr][pc] = game_consts.TILE_EMPTY

    # 3x4 diamond block cleanly at the end
    for r in range(rows - 3, rows):
        for c in range(cols - 4, cols):
            grid[r][c] = game_consts.TILE_DIAMOND

    return grid