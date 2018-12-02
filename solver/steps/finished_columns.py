from puzzle_state import PuzzleState
from enums.slot_state import SlotState
from steps.step import Step


class FinishedColumns(Step):
    """
    Blocks empty slots in columns that already have the desired number of ships placed.
    """
    def check_for_next_step(self, grid_state: PuzzleState):
        for column, count in enumerate(grid_state.puzzle.counts_columns):
            if count == grid_state.current_counts_columns[column]:
                return True
        return False

    def do_next_step(self, grid_state: PuzzleState):
        for column, count in enumerate(grid_state.puzzle.counts_columns):
            if count == grid_state.current_counts_columns[column]:
                for row in range(grid_state.puzzle.rows):
                    if grid_state.state[column][row] == SlotState.EMPTY.value:
                        grid_state.state[column][row] = SlotState.WATER.value
