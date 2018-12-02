from enums.puzzle_param import PuzzleParam
from solver.solver import BattleShipSolver

# amount of ships for each size (e.g. {1: 2, 2: 3} = > two ships of size 1 and three of size two)
ships = {2: 1, 5: 1, 3: 1}
grid_columns = 5  # number of columns in the grid
grid_rows = grid_columns  # number of rows in the grid
counts_columns = [1, 4, 1, 3, 1]  # number of ship elements from left to right
counts_rows = [2, 2, 1, 0, 5]  # number of ship elements from top to bottom

puzzle = {
    PuzzleParam.SHIPS.value: ships,
    PuzzleParam.COLUMNS.value: grid_columns,
    PuzzleParam.ROWS.value: grid_rows,
    PuzzleParam.COUNTS_COLUMNS.value: counts_columns,
    PuzzleParam.COUNTS_ROWS.value: counts_rows
}
BattleShipSolver(puzzle, debug=True).start()
