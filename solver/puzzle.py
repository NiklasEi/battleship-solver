from typing import Dict

from enums.puzzle_param import PuzzleParam
from puzzle_state import PuzzleState


class Puzzle:
    """
    Represents a puzzle
    """
    def __init__(self, puzzle: Dict):
        self.columns = puzzle[PuzzleParam.COLUMNS.value]
        self.rows = puzzle[PuzzleParam.ROWS.value]
        self.counts_columns = puzzle[PuzzleParam.COUNTS_COLUMNS.value]
        self.counts_rows = puzzle[PuzzleParam.COUNTS_ROWS.value]
        self.ships = puzzle[PuzzleParam.SHIPS.value]
        if PuzzleParam.INITIAL_STATE in puzzle:
            self.initial_state = PuzzleState(self, self.ships, initial_state=puzzle[PuzzleParam.INITIAL_STATE.value])
        else:
            self.initial_state = PuzzleState(self, self.ships)
        self.current_state = self.initial_state

    def is_solved(self) -> bool:
        # ToDo: when getting to have to guess possible solutions one needs more then one state here
        #    For now just return, whether there are ships left to place
        return not any(self.current_state.left_ships)

    # ToDo: getting neighboring slots should be grid's responsibility
