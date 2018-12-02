from solver.grid_state import GridState


class Grid:
    """
    Represents a puzzle grid
    """
    def __init__(self, columns, rows, counts_columns, counts_rows, ships):
        self.columns = columns
        self.rows = rows
        self.counts_columns = counts_columns
        self.counts_rows = counts_rows
        self.ships = ships
        self.initial_state = GridState(grid=self, ships=ships)
        self.current_state = self.initial_state

    def is_solved(self) -> bool:
        # ToDo: when getting to have to guess possible solutions one needs more then one state here
        #    For now just return, whether there are ships left to place
        return not any(self.current_state.left_ships)

    # ToDo: getting neighboring slots should be grid's responsibility
