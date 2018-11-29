from solver.solver import BattleShipSolver

# amount of ships for each size (e.g. {1: 2, 2: 3} = > two ships of size 1 and three of size two)
ships = {2: 2, 5: 1}
grid_columns = 5  # number of columns in the grid
grid_rows = grid_columns  # number of rows in the grid
counts_columns = [1, 3, 1, 3, 1]  # number of ship elements from left to right
counts_rows = [2, 2, 0, 0, 5]  # number of ship elements from top to bottom

BattleShipSolver(grid_columns, grid_rows, ships, counts_columns, counts_rows).start()
