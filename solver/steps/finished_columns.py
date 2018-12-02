from puzzle_state import PuzzleState
from enums.slot_state import SlotState
from steps.step import Step


class FinishedColumns(Step):
    """
    Blocks empty slots in columns that already have the desired number of ships placed.
    """
    def check_for_next_step(self, puzzle_state: PuzzleState):
        for column, count in enumerate(puzzle_state.puzzle.counts_columns):
            if count == puzzle_state.current_counts_columns[column]:
                for row in range(puzzle_state.puzzle.rows):
                    if puzzle_state.state[column][row] == SlotState.EMPTY.value:
                        return True
        return False

    def do_next_step(self, puzzle_state: PuzzleState):
        for column, count in enumerate(puzzle_state.puzzle.counts_columns):
            if count == puzzle_state.current_counts_columns[column]:
                for row in range(puzzle_state.puzzle.rows):
                    if puzzle_state.state[column][row] == SlotState.EMPTY.value:
                        puzzle_state.state[column][row] = SlotState.WATER.value
