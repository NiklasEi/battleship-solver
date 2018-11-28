from solver.grid import Grid
import time


class BattleShipSolver:
    def __init__(self, grid_columns, grid_rows, ships, counts_columns, counts_rows):
        self.ships = ships
        self.grid_columns = grid_columns
        self.grid_rows = grid_rows
        self.counts_columns = counts_columns
        self.counts_rows = counts_rows

        assert len(self.counts_columns) == self.grid_columns, \
            "number of column counts does not equal the number of columns"
        assert len(self.counts_rows) == self.grid_rows, \
            "number of row counts does not equal the number of rows"
        assert all(isinstance(item, int) for item in self.counts_columns), \
            "There is a invalid value in the column counts"
        assert all(isinstance(item, int) for item in self.counts_rows), \
            "There is a invalid value in the row counts"

        # other instance attributes
        self.start_time = None
        self.grid = None

    def start(self):
        self.start_time = time.time()
        self.grid = Grid(self.grid_columns, self.grid_rows, self.counts_columns, self.counts_rows, self.ships)
        self.print_currently_used_time()

    def print_currently_used_time(self):
        print("Ran for: {} seconds".format(str(time.time() - self.start_time)))

