from typing import Dict, List

from puzzle_state import PuzzleState
from steps.step import Step


class FillUpShips(Step):
    """
    This step checks if the number of free slots in a row or column is equal to the number of missing ship parts.
    """

    def __init__(self):
        """
        In order to not look up all free lines in columns/rows on checking AND on filling, the new data
        will be pulled once on prepare and then saved in instance variables.
        """
        self.currently_free_lines_in_columns: Dict[int, Dict[int, List[List[List[int]]]]] = {}
        self.currently_free_lines_in_rows: Dict[int, Dict[int, List[List[List[int]]]]] = {}
        self.currently_missing_ships_in_columns: List[int] = []
        self.currently_missing_ships_in_rows: List[int] = []

    def check_for_next_step(self, grid_state: PuzzleState) -> bool:
        for column in range(grid_state.puzzle.columns):
            if 0 < self.currently_missing_ships_in_columns[column] \
                    == FillUpShips.count_slots_in_lines(self.currently_free_lines_in_columns[column]):
                if not self.are_correct_ships_missing(grid_state, self.currently_free_lines_in_columns[column]):
                    continue
        for row in range(grid_state.puzzle.rows):
            if 0 < self.currently_missing_ships_in_rows[row] == \
                    FillUpShips.count_slots_in_lines(self.currently_free_lines_in_rows[row]):
                if not self.are_correct_ships_missing(grid_state, self.currently_free_lines_in_columns[column]):
                    continue
        return False

    def do_next_step(self, grid_state: PuzzleState):
        changes = False
        for column in range(grid_state.puzzle.columns):
            if 0 < self.currently_missing_ships_in_columns[column] \
                    == FillUpShips.count_slots_in_lines(self.currently_free_lines_in_columns[column]):
                if not self.are_correct_ships_missing(grid_state, self.currently_free_lines_in_columns[column]):
                    continue
                grid_state.place_ships(self.currently_free_lines_in_columns[column])
                changes = True
        # if ships in columns were set, update the empty lines and counts
        # ToDo: when specific ship parts start to count, it will be important to go from longest ship to smallest
        if changes:
            self.prepare(grid_state)
        for row in range(grid_state.puzzle.rows):
            if 0 < self.currently_missing_ships_in_rows[row] == \
                    FillUpShips.count_slots_in_lines(self.currently_free_lines_in_rows[row]):
                if not self.are_correct_ships_missing(grid_state, self.currently_free_lines_in_rows[row]):
                    continue
                grid_state.place_ships(self.currently_free_lines_in_rows[row])

    def prepare(self, grid_state: PuzzleState):
        for column in range(grid_state.puzzle.columns):
            self.currently_free_lines_in_columns[column] = grid_state.get_free_lines({"columns": [column]})
        for row in range(grid_state.puzzle.rows):
            self.currently_free_lines_in_rows[row] = grid_state.get_free_lines({"rows": [row]})
        self.currently_missing_ships_in_columns \
            = [count - placed for (count, placed)
               in zip(grid_state.puzzle.counts_columns, grid_state.current_counts_columns)]
        self.currently_missing_ships_in_rows \
            = [count - placed for (count, placed)
               in zip(grid_state.puzzle.counts_rows, grid_state.current_counts_rows)]

    @staticmethod
    def are_correct_ships_missing(grid_state: PuzzleState, free_lines: Dict[int, List[List[List[int]]]]) -> bool:
        for line_length, line_positions in free_lines.items():
            if line_length not in grid_state.left_ships:
                return False
            elif grid_state.left_ships[line_length] < len(line_positions):
                return False
        return True

    @staticmethod
    def count_slots_in_lines(lines: Dict[int, List[List[List[int]]]]) -> int:
        return sum([line_length * len(lines) for (line_length, lines) in lines.items()])
