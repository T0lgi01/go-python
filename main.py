EMPTY, BLACK, WHITE = 0, 1, 2

class Board:
    def __init__(self):
        self.Board = [[EMPTY for _ in range(19)] for _ in range(19)]
        self.Black_Cap = 0
        self.White_Cap = 0
        self.Move_Color = BLACK
        self.checked = []

    def __repr__(self):
        for k in range(361):
            i, j = divmod(k, 19)
            which = self.Board[i][j] + 3*int((i%6, j%6, self.Board[i][j]) == (3, 3, EMPTY))
            print(".#O*"[which], end = " \n"[int(j % 19 == 18)])

        print("Prisoners. B: {}, W: {}\nCurrent Move: {}".format(
            self.Black_Cap, self.White_Cap, ["BLACK", "WHITE"][self.Move_Color == WHITE]
        ))
    
    def has_liberty(self, x, y, checked = []):
        current_cell_color = self.Board[y][x]
        if current_cell_color == EMPTY: return True
        checked.append((x, y))
        for k in range(4):
            x_off, y_off = x + [0, 1, 0, -1][k], y + [1, 0, -1, 0][k]
            if not 0 <= x_off < 19 > y_off >= 0: continue
            if self.Board[y_off][x_off] == EMPTY: return True
            if self.Board[y_off][x_off] == current_cell_color \
                and (not (x_off, y_off) in checked):
                has_liberty = self.has_liberty(x_off, y_off, checked)
                if has_liberty: return True
        return False

    def play_move(self, x, y):
        if self.Board[y][x] != EMPTY:
            print("Cannot place stone at {}, {}!".format(x, y))
            return False
        
        self.Board[y][x] = self.Move_Color
        is_kill = False

        for k in range(4):
            x_off, y_off = x + [0, 1, 0, -1][k], y + [1, 0, -1, 0][k]
            if not 0 <= x_off < 19 > y_off >= 0: continue
            if not self.Board[y_off][x_off] in (EMPTY, self.Move_Color):
                checked = []
                has_liberty = self.has_liberty(x_off, y_off, checked)
                if has_liberty: continue
                is_kill = True
                if self.Move_Color == BLACK: 
                    self.Black_Cap += len(checked)
                else: 
                    self.White_Cap += len(checked)
                for check in checked:
                    self.Board[check[1]][check[0]] = EMPTY
        
        if not is_kill:
            has_liberty = self.has_liberty(x, y, [])
            if not has_liberty:
                print("Suicide move at {}, {}!".format(x, y))
                self.Board[y][x] = EMPTY
                return False
        
        print("Played move at {}, {}.".format(x, y))
        self.Move_Color ^= 3
        return True

def main():
    B = Board()
    moves = [(2, 0), (3, 0), (1, 0), (2, 1), (13, 17), (1, 1), (0, 0), (0, 1)]
    for move in moves:
        B.play_move(*move)
    B.__repr__()

main()