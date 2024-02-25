EMPTY, BLACK, WHITE = 0, 1, 2

def in_bounds(x, y): return 0 <= x < 19 > y >= 0

class Board:
    def __init__(self):
        self.Board = [[EMPTY for _ in range(19)] for _ in range(19)]
        self.Cap = [0, 0] # Black, White
        self.Move_Color = BLACK

    def __repr__(self):
        for k in range(361):
            i, j = divmod(k, 19)
            which = self.Board[i][j] + \
                3*int((i%6, j%6, self.Board[i][j]) == (3, 3, EMPTY))
            print(".#O*"[which], end = " \n"[int(j % 19 == 18)])
        print("Prisoners. B: {}, W: {}\nCurrent Move: {}".format(
            *self.Cap, ["BLACK", "WHITE"][self.Move_Color == WHITE]))
    
    def has_liberty(self, x, y, checked = []):
        if (current_cell_color := self.Board[y][x]) == EMPTY: return True
        checked.append((x, y))
        for k in range(4):
            if not in_bounds(x_off := x + [0, 1, 0, -1][k], 
                             y_off := y + [1, 0, -1, 0][k]): continue
            if self.Board[y_off][x_off] == EMPTY \
                or self.Board[y_off][x_off] == current_cell_color \
                and (not (x_off, y_off) in checked) \
                and self.has_liberty(x_off, y_off, checked):
                    return True
        return False

    def play_move(self, x, y):
        if not in_bounds(x, y): 
            return False, "Out Of Bounds at {}, {}!".format(x, y)
        if self.Board[y][x] != EMPTY:
            return False, "Cannot place stone at {}, {}!".format(x, y)
        
        self.Board[y][x] = self.Move_Color
        is_kill = False
        for k in range(4):
            if not in_bounds(x_off := x + [0, 1, 0, -1][k], 
                             y_off := y + [1, 0, -1, 0][k]): continue
            if self.Board[y_off][x_off] == self.Move_Color^3:
                if self.has_liberty(x_off, y_off, checked := []): continue
                is_kill = True
                self.Cap[int(self.Move_Color == WHITE)] += len(checked)
                for check in checked:
                    self.Board[check[1]][check[0]] = EMPTY
        
        if not is_kill and not self.has_liberty(x, y):
            self.Board[y][x] = EMPTY
            return False, "Suicide move at {}, {}!".format(x, y)
        self.Move_Color ^= 3
        return True, "Played move at {}, {}.".format(x, y)

def main():
    B = Board()
    moves = [(2, 0), (3, 0), (1, 0), (2, 1), (13, 17), (1, 1), (0, 0), (0, 1)]
    for move in moves:
        B.play_move(*move)
    #B.__repr__()
    print()

    moves2 = [(18, 17), (18, 18), (17, 18), (18, 18)]
    for move in moves2:
        print(B.play_move(*move)[1])
    B.__repr__()

main()