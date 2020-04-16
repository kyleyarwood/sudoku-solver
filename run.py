from PyQt5.QtWidgets import *
from sudoku_solver import SudokuSolver
from PyQt5.QtCore import Qt

class SudokuGui(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("Sudoku Solver")
		self.widget_cells = []
		self.window = QWidget(self)
		self._set_to_initial_layout()
		self.solver = SudokuSolver()

	def _replace_layout(self, layout):
		window = QWidget(self)
		window.setLayout(layout)
		self.window = window
		self.window.setFocus()
		self.setCentralWidget(self.window)

	def _set_to_initial_layout(self):
		self._replace_layout(self._get_initial_layout())

	def _get_initial_layout(self):
		vertical_layout = QVBoxLayout()
		vertical_layout.setSpacing(0)
		vertical_layout.addStretch(1)
		self.widget_cells = []
		for i in range(9):
			horizontal_layout = QHBoxLayout()
			horizontal_layout.setSpacing(0)
			horizontal_layout.addStretch(1)
			widget_row = []
			for j in range(9):
				le = QLineEdit('')
				le.setMaxLength(1)
				le.setAlignment(Qt.AlignCenter)
				widget_row.append(le)
				horizontal_layout.addWidget(widget_row[-1])
			vertical_layout.addLayout(horizontal_layout)
			self.widget_cells.append(widget_row)
		vertical_layout.addWidget(self._get_solve_button())
		return vertical_layout

	def _get_solve_button(self):
		solve_button = QPushButton('Solve')
		solve_button.clicked.connect(self._solve)
		return solve_button

	def get_window(self):
		return self.window

	def _encode(self):
		puzzle_encoding = []
		for widget_row in self.widget_cells:
			new_row = []
			for cell in widget_row:
				text = cell.text()
				if text in list(map(str, range(1, 9+1))):
					new_row.append(int(text))
				else:
					new_row.append(None)
			puzzle_encoding.append(new_row)
		return puzzle_encoding

	def _display_solution(self, solution):
		vertical_layout = QVBoxLayout()
		for row in solution:
			horizontal_layout = QHBoxLayout()
			for cell in row:
				le = QLineEdit(str(cell))
				le.setReadOnly(True)
				horizontal_layout.addWidget(le)
			vertical_layout.addLayout(horizontal_layout)
		new_puzzle_btn = QPushButton('New Puzzle!')
		new_puzzle_btn.clicked.connect(self._set_to_initial_layout)
		vertical_layout.addWidget(new_puzzle_btn)
		self._replace_layout(vertical_layout)			

	def _solve(self):
		puzzle_encoding = self._encode()
		print("Solving...")
		if not self.solver.is_valid_sudoku(puzzle_encoding):
			QMessageBox.about(self, "Invalid", "Please enter a valid puzzle")
			return
		solved_puzzle, solved = self.solver.solve_sudoku(puzzle_encoding)
		if not solved:
			QMessageBox.about(self, "Unsolvable", "Can't solve this puzzle! Try again")
			return
		self._display_solution(solved_puzzle)

def main():
	app = QApplication([])
	sudoku_gui = SudokuGui()
	sudoku_gui.show()
	app.exec_()

if __name__ == "__main__":
	main()
