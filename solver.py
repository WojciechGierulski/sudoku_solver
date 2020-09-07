from viability_check import check_viable_numbers
import time


TIMEOUT = 0.01  # The shorter the timeout the faster the animation

def solve(board, solving, rows=9):
    run = True
    x, y = determine_first(board, rows)
    while run:
        # check result
        time.sleep(TIMEOUT)
        if y == -1:
            break
        elif y == rows:
            break
        box = board[x][y]
        if box.number is None:
            box.viable_numbers = check_viable_numbers(box, board, rows)
        if len(box.viable_numbers) == 0:
            x, y = go_backwards(x, y, board)
            continue
        else:
            if box.number is None:
                box.number = get_first_from_set(box.viable_numbers)
                x, y = go_forward(x, y, board)
                continue
            else:
                box.viable_numbers.remove(box.number)
                box.number = None
                if len(box.viable_numbers) == 0:
                    x, y = go_backwards(x, y, board)
                    continue
                else:
                    box.number = get_first_from_set(box.viable_numbers)
                    x, y = go_forward(x, y, board)
                    continue
    solving[0] = False
    solving[1] = True


def go_forward(x, y, board):
    if x == 8:
        new_x = 0
        new_y = y + 1
    else:
        new_x = x + 1
        new_y = y
    try:
        if not board[new_x][new_y].block:
            return new_x, new_y
        else:
            return go_forward(new_x, new_y, board)
    except Exception:
        return 0, 9


def go_backwards(x, y, board):
    if x == 0:
        new_x = 8
        new_y = y - 1
    else:
        new_x = x - 1
        new_y = y
    if not board[new_x][new_y].block:
        return new_x, new_y
    else:
        return go_backwards(new_x, new_y, board)


def get_first_from_set(s):
    for e in s:
        break
    return e


def determine_first(board, rows):
    for y in range(rows):
        for x in range(rows):
            if not board[x][y].block:
                return x, y
    return rows - 1, rows - 1
