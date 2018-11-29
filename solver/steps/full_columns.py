from grid_state import GridState
from steps.step import Step


class FullColumns(Step):
    def check_for_next_step(self, grid_state: GridState) -> bool:
        for column, count in enumerate(grid_state.grid.counts_columns):
            if count == grid_state.grid.rows:
                return True
        return False

    def do_next_step(self, grid_state: GridState):
        for column, count in enumerate(grid_state.grid.counts_columns):
            if count == grid_state.grid.rows:
                ship_position = []
                for row in range(grid_state.grid.rows):
                    ship_position.append([column, row])
                grid_state.place_ships({grid_state.grid.rows: [ship_position]})
