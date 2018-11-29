from solver.grid_state import GridState


class Grid:
    def __init__(self, columns, rows, counts_columns, counts_rows, ships):
        self.columns = columns
        self.rows = rows
        self.counts_columns = counts_columns
        self.counts_rows = counts_rows
        self.ships = ships
        self.initial_state = GridState(grid=self, ships=ships)
        self.current_state = self.initial_state
