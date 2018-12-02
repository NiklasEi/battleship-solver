from puzzle_state import PuzzleState
from enums.slot_state import SlotState
from steps.step import Step


class FinishedRows(Step):
    """
    Blocks empty slots in rows that already have the desired number of ships placed.
    """
    def check_for_next_step(self, puzzle_state: PuzzleState):
        for row, count in enumerate(puzzle_state.puzzle.counts_rows):
            if count == puzzle_state.current_counts_rows[row]:
                for column in range(puzzle_state.puzzle.columns):
                    if puzzle_state.state[column][row] == SlotState.EMPTY.value:
                        return True
        return False

    def do_next_step(self, puzzle_state: PuzzleState):
        for row, count in enumerate(puzzle_state.puzzle.counts_rows):
            if count == puzzle_state.current_counts_rows[row]:
                for column in range(puzzle_state.puzzle.columns):
                    if puzzle_state.state[column][row] == SlotState.EMPTY.value:
                        puzzle_state.state[column][row] = SlotState.WATER.value
