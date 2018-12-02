from typing import Dict, List

from puzzle_state import PuzzleState
from steps.step import Step


class FillUpShips(Step):
    """
    This step checks if the number of free slots in a row or column is equal to the number of missing ship parts.
    """

    def check_for_next_step(self, puzzle_state: PuzzleState) -> bool:
        for column in range(puzzle_state.puzzle.columns):
            if 0 < puzzle_state.currently_missing_ships_in_columns[column] \
                    == FillUpShips.count_slots_in_lines(puzzle_state.currently_free_lines_in_columns[column]):
                if not self.are_correct_ships_missing(puzzle_state, puzzle_state.currently_free_lines_in_columns[column]):
                    continue
        for row in range(puzzle_state.puzzle.rows):
            if 0 < puzzle_state.currently_missing_ships_in_rows[row] == \
                    FillUpShips.count_slots_in_lines(puzzle_state.currently_free_lines_in_rows[row]):
                if not self.are_correct_ships_missing(puzzle_state, puzzle_state.currently_free_lines_in_rows[row]):
                    continue
        return False

    def do_next_step(self, puzzle_state: PuzzleState):
        changes = False
        for column in range(puzzle_state.puzzle.columns):
            if 0 < puzzle_state.currently_missing_ships_in_columns[column] \
                    == FillUpShips.count_slots_in_lines(puzzle_state.currently_free_lines_in_columns[column]):
                if not self.are_correct_ships_missing(puzzle_state, puzzle_state.currently_free_lines_in_columns[column]):
                    continue
                puzzle_state.place_ships(puzzle_state.currently_free_lines_in_columns[column])
                changes = True
        # if ships in columns were set, update the empty lines and counts
        # ToDo: when specific ship parts start to count, it will be important to go from longest ship to smallest
        if changes:
            puzzle_state.update()
        for row in range(puzzle_state.puzzle.rows):
            if 0 < puzzle_state.currently_missing_ships_in_rows[row] == \
                    FillUpShips.count_slots_in_lines(puzzle_state.currently_free_lines_in_rows[row]):
                if not self.are_correct_ships_missing(puzzle_state, puzzle_state.currently_free_lines_in_rows[row]):
                    continue
                puzzle_state.place_ships(puzzle_state.currently_free_lines_in_rows[row])

    @staticmethod
    def are_correct_ships_missing(puzzle_state: PuzzleState, free_lines: Dict[int, List[List[List[int]]]]) -> bool:
        for line_length, line_positions in free_lines.items():
            if line_length not in puzzle_state.missing_ships:
                return False
            elif puzzle_state.missing_ships[line_length] < len(line_positions):
                return False
        return True

    @staticmethod
    def count_slots_in_lines(lines: Dict[int, List[List[List[int]]]]) -> int:
        return sum([line_length * len(lines) for (line_length, lines) in lines.items()])
