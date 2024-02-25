EMPTY, BLACK, WHITE = 0, 1, 2

def in_bounds(x, y): return 0<=x<19>y>=0

class Board:
    def __init__(self):
        self.Board = [[EMPTY for _ in range(19)] for _ in range(19)]
        self.Cap = [0, 0] # Black, White
        self.Move_Color = BLACK

    def __repr__(self):
        for k in range(361):
            i, j = divmod(k, 19)
            which = self.Board[i][j] + 3*((i%6, j%6) == (3, 3))
            print(".#O*#O"[which], end = " \n"[j%19 == 18])
        print("Prisoners. B: {}, W: {}\nCurrent Move: {}".format(
            *self.Cap, ["BLACK", "WHITE"][self.Move_Color == WHITE]))
    
    def has_liberty(self, x, y, checked = []):
        if (current_cell := self.Board[y][x]) == EMPTY: return True
        checked.append((x, y))
        for x_off, y_off in ((x, y+1), (x+1, y), (x, y-1), (x-1, y)):
            if in_bounds(x_off, y_off) \
                and (self.Board[y_off][x_off] == EMPTY \
                or self.Board[y_off][x_off] == current_cell \
                and (not (x_off, y_off) in checked) \
                and self.has_liberty(x_off, y_off, checked)):
                return True
        return False

    def play_move(self, x, y):
        if not in_bounds(x, y): 
            return False, "Out Of Bounds at {}, {}!".format(x, y)
        if self.Board[y][x] != EMPTY:
            return False, "Cannot place stone at {}, {}!".format(x, y)
        
        self.Board[y][x] = self.Move_Color
        is_kill = False
        for x_off, y_off in ((x, y+1), (x+1, y), (x, y-1), (x-1, y)):
            if in_bounds(x_off, y_off) \
                and self.Board[y_off][x_off] == self.Move_Color^3 \
                and not self.has_liberty(x_off, y_off, checked := []):
                is_kill = True
                self.Cap[self.Move_Color == WHITE] += len(checked)
                for stone_x, stone_y in checked:
                    self.Board[stone_y][stone_x] = EMPTY
        
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