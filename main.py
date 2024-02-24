EMPTY = 0
BLACK = 1
WHITE = 2

def setup_game():
    return [[EMPTY for _ in range(19)] for _ in range(19)], 0, 0, BLACK

def in_bounds(x, y):
    return 0 <= x < 19 > y >= 0

def board_print(Board, Black_Cap, White_Cap, Move_Color):
    for i in range(19):
        for j in range(19):
            #which = (Board[i][j] + 3*int(i%6==3 and j%6==3 and Board[i][j] == EMPTY))
            which = Board[i][j] + 3*int((i%6, j%6, Board[i][j]) == (3, 3, EMPTY))
            print(".#O*"[which], end = " \n"[int(j % 19 == 18)])
    print("Prisoners. B: {}, W: {}\nCurrent Move: {}".format(
        Black_Cap, White_Cap, ["BLACK", "WHITE"][Move_Color == WHITE]
    ))

def board_has_liberty(Board, x, y, Move_Color, checked):
    current_cell_color = Board[y][x]
    if current_cell_color == EMPTY: return True, checked
    checked.append((x, y))
    for k in range(4):
        x_off, y_off = x + [0, 1, 0, -1][k], y + [1, 0, -1, 0][k]
        if not in_bounds(x, y): continue
        if Board[y_off][x_off] == EMPTY: return True, checked
        if Board[y_off][x_off] != Move_Color \
            and not (x_off, y_off) in checked:
            has_liberty, checked = \
                board_has_liberty(Board, x_off, y_off, Move_Color, checked)
            if has_liberty: return True, checked
    return False, checked

def board_play_move(Board, x, y, Move_Color, Black_Cap, White_Cap):
    if Board[y][x] != EMPTY:
        print("Cannot place stone at {}, {}!".format(x, y))
        return False, Board, Black_Cap, White_Cap
    
    Board[y][x] = Move_Color
    is_kill = False

    for k in range(4):
        x_off, y_off = x + [0, 1, 0, -1][k], y + [1, 0, -1, 0][k]
        if not in_bounds(x, y): continue
        if Board[y_off][x_off] not in (EMPTY, Move_Color):
            has_liberty, checked = \
                board_has_liberty(Board, x_off, y_off, Move_Color, checked)
            if has_liberty: continue
            is_kill = True
            if Move_Color == BLACK: Black_Cap += len(checked)
            else: White_Cap += len(checked)
            for check in checked:
                Board[check[1]][check[0]] = EMPTY
    
    if not is_kill:
        has_liberty, _ = board_has_liberty(Board, x, y, Move_Color, [])
        if not has_liberty:
            print("Suicide move at {}, {}!".format(x, y))
            Board[y][x] = EMPTY
            return False, Board, Black_Cap, White_Cap
    
    print("Played move at {}, {}.".format(x, y))
    Move_Color ^= 3
    return True, Board, Black_Cap, White_Cap


def main():
    Board, Black_Cap, White_Cap, Move_Color = setup_game()
    _, Board, Black_Cap, White_Cap = board_play_move(Board, 2, 0, BLACK, Black_Cap, White_Cap)
    board_print(Board, Black_Cap, White_Cap, Move_Color)


main()