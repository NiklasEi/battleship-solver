from typing import Dict

from enums.puzzle_param import PuzzleParam
from enums.slot_state import SlotState
from runner import Runner
from solver.puzzle import Puzzle
import time


class BattleShipSolver:
    """
    This class represents the solver.

    It directly controls the runners, that can run the different logic steps
    to solve a battleship puzzle.
    """
    def __init__(self, puzzle_data: Dict, debug=False):
        self.puzzle_data = puzzle_data
        self.debug = debug

        # check given puzzle for correct dimensions and value issues
        assert len(puzzle_data[PuzzleParam.COUNTS_COLUMNS.value]) == puzzle_data[PuzzleParam.COLUMNS.value], \
            "number of column counts does not equal the number of columns"
        assert len(puzzle_data[PuzzleParam.COUNTS_ROWS.value]) == puzzle_data[PuzzleParam.ROWS.value], \
            "number of row counts does not equal the number of rows"
        assert all(isinstance(item, int) for item in puzzle_data[PuzzleParam.COUNTS_COLUMNS.value]), \
            "There is a invalid value in the column counts"
        assert all(isinstance(item, int) for item in puzzle_data[PuzzleParam.COUNTS_ROWS.value]), \
            "There is a invalid value in the row counts"
        if PuzzleParam.INITIAL_STATE.value in puzzle_data:
            assert len(puzzle_data[PuzzleParam.INITIAL_STATE.value]) == puzzle_data[PuzzleParam.ROWS.value], \
                "The initial state has a different number of rows then the puzzle"
            for row in puzzle_data[PuzzleParam.INITIAL_STATE.value]:
                assert len(row) == puzzle_data[PuzzleParam.COLUMNS.value], \
                    "The initial state has a different number of columns then the puzzle"
            try:
                [[SlotState(string) for string in list(row)] for row in puzzle_data[PuzzleParam.INITIAL_STATE.value]]
            except ValueError:
                raise ValueError("Initial state of puzzle contains unknown slot state")

        # other instance attributes
        self.start_time = None
        self.runner = None
        self.puzzle = None
        self.prepare_runner()

    def start(self):
        self.start_time = time.time()
        self.puzzle = Puzzle(self.puzzle_data)
        while not self.puzzle.is_solved():
            self.runner.run(self.puzzle.current_state)
            self.puzzle.current_state.display()
            self.print_currently_used_time()
            if time.time() - self.start_time > 0.5:
                break
        print("Done!")

    def print_currently_used_time(self):
        print("Ran for: {} seconds".format(str(time.time() - self.start_time)))

    def prepare_runner(self):
        self.runner = Runner()
        from steps.fill_up_ships import FillUpShips
        self.runner.add_step(FillUpShips())
        from steps.finished_columns import FinishedColumns
        self.runner.add_step(FinishedColumns())
        from steps.finished_rows import FinishedRows
        self.runner.add_step(FinishedRows())
        from steps.place_longest_ships import PlaceLongestShips
        self.runner.add_step(PlaceLongestShips())
