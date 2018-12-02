from grid_state import GridState
from enums.slot_state import SlotState
from steps.step import Step


class FinishedColumns(Step):
    """
    Blocks empty slots in columns that already have the desired number of ships placed.
    """
    def check_for_next_step(self, grid_state: GridState):
        for column, count in enumerate(grid_state.grid.counts_columns):
            if count == grid_state.current_counts_columns[column]:
                return True
        return False

    def do_next_step(self, grid_state: GridState):
        for column, count in enumerate(grid_state.grid.counts_columns):
            if count == grid_state.current_counts_columns[column]:
                for row in range(grid_state.grid.rows):
                    if grid_state.state[column][row] == SlotState.EMPTY.value:
                        grid_state.state[column][row] = SlotState.WATER.value
