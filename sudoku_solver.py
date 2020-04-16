class SudokuSolver:
    def __init__(self):
        pass

    def is_valid_sudoku(self, board):
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if cell is not None and cell not in self.get_options(board, (i,j)):
                    return False
        return True

    def get_options(self, board, cell):
        options = set(range(1, 9+1))
        for i in range(9):
            if i != cell[1] and board[cell[0]][i] in options:
                options.remove(board[cell[0]][i])
            if i != cell[0] and board[i][cell[1]] in options:
                options.remove(board[i][cell[1]])
            if ((3*(cell[0]//3)+i%3 != cell[0] or 3*(cell[1]//3)+i//3 != cell[1])
                and board[3*(cell[0]//3)+i%3][3*(cell[1]//3)+i//3] in options):
                options.remove(board[3*(cell[0]//3)+i%3][3*(cell[1]//3)+i//3])
        return list(options)

    def sudoku_is_solved(self, board):
        for row in board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def get_min_options_cell_with_options(self, board):
        min_options_cell, options_for_cell = None, list(range(1, 11))
        for i in range(9):
            for j in range(9):
                if board[i][j] is not None:
                    continue
                options = self.get_options(board, (i, j))
                if len(options) < len(options_for_cell):
                    min_options_cell, options_for_cell = (i, j), options
        return min_options_cell, options_for_cell

    def solve_sudoku(self, board):
        if self.sudoku_is_solved(board):
            return board, True
        min_options_cell, options_for_cell = self.get_min_options_cell_with_options(board)

        for option in options_for_cell:
            board[min_options_cell[0]][min_options_cell[1]] = option
            new_board, solved = self.solve_sudoku(board)
            if solved:
                return new_board, solved
            board[min_options_cell[0]][min_options_cell[1]] = None

        return board, False

    def get_board(self, filename):
        with open(filename, 'r') as f:
            inp = f.readlines()
        board = [list(None if c=='-' else int(c) for c in line.strip())
                     for line in inp]
        return board

    def print_board(self, board):
        for row in board:
            print(''.join(map(str, row)))
