from grid_state import GridState
from steps.step import Step


class FullRows(Step):
    def check_for_next_step(self, grid_state: GridState):
        for row, count in enumerate(grid_state.grid.counts_rows):
            if count == grid_state.grid.columns:
                return True
        return False

    def do_next_step(self, grid_state: GridState):
        for row, count in enumerate(grid_state.grid.counts_rows):
            if count == grid_state.grid.columns:
                ship_position = []
                for column in range(grid_state.grid.columns):
                    ship_position.append([column, row])
                grid_state.place_ships({grid_state.grid.columns: [ship_position]})
