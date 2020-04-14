def get_options(board, cell):
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

def sudoku_is_solved(board):
	for row in board:
		for cell in row:
			if cell is None:
				return False
	return True

def get_min_options_cell_with_options(board):
	min_options_cell, options_for_cell = None, list(range(1, 11))
	for i in range(9):
		for j in range(9):
			if board[i][j] is not None:
				continue
			options = get_options(board, (i, j))
			if len(options) < len(options_for_cell):
				min_options_cell, options_for_cell = (i, j), options
	return min_options_cell, options_for_cell

def solve_sudoku(board):
	if sudoku_is_solved(board):
		return board, True
	min_options_cell, options_for_cell = get_min_options_cell_with_options(board)

	for option in options_for_cell:
		board[min_options_cell[0]][min_options_cell[1]] = option
		new_board, solved = solve_sudoku(board)
		if solved:
			return new_board, solved
		board[min_options_cell[0]][min_options_cell[1]] = None

	return board, False

def get_board(filename):
	with open(filename, 'r') as f:
		inp = f.readlines()
	board = [list(None if c=='-' else int(c) for c in line.strip())
					 for line in inp]
	return board

def print_board(board):
	for row in board:
		print(''.join(map(str, row)))

def main():
	board = get_board('test.in')
	result,solved = solve_sudoku(board)
	print_board(result)

if __name__ == "__main__":
	main()
