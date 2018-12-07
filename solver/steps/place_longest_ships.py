from typing import Dict, List

from puzzle_state import PuzzleState
from impossible_puzzle_exception import ImpossiblePuzzleException
from steps.step import Step


class PlaceLongestShips(Step):
    """
    Checks whether there are only as many possible lines left for the
    longest ship, as there are ships left to place for that length.
    """

    def __init__(self):
        """
        In order to not look up all free lines in columns/rows on checking AND on filling, the new data
        will be pulled once on prepare and then saved in instance variables.
        """
        self.relevant_free_lines_in_columns: Dict[int, Dict[int, List[List[List[int]]]]] = {}
        self.relevant_free_lines_in_rows: Dict[int, Dict[int, List[List[List[int]]]]] = {}

    def check_for_next_step(self, grid_state: PuzzleState):
        max_ship_length = max(grid_state.missing_ships.keys())
        # print(str(grid_state.free_lines))
        max_length_free_line = max(grid_state.free_lines.keys())
        if max_length_free_line == max_ship_length:
            ship_count = grid_state.missing_ships[max_ship_length]
            free_lines_count = sum([len(free_lines[max_length_free_line] if max_length_free_line in free_lines else ())
                                    for free_lines in self.relevant_free_lines_in_columns.values()])
            free_lines_count += sum([len(free_lines[max_length_free_line] if max_length_free_line in free_lines else ())
                                    for free_lines in self.relevant_free_lines_in_rows.values()])
            if free_lines_count == ship_count:
                return True
        return False

    def do_next_step(self, grid_state: PuzzleState):
        max_ship_length = max(grid_state.missing_ships.keys())
        max_length_free_line = max(grid_state.free_lines.keys())
        if max_length_free_line == max_ship_length:
            ship_count = grid_state.missing_ships[max_ship_length]
            free_lines_count = sum([len(free_lines[max_length_free_line] if max_length_free_line in free_lines else ())
                                    for free_lines in self.relevant_free_lines_in_columns.values()])
            free_lines_count += sum([len(free_lines[max_length_free_line] if max_length_free_line in free_lines else ())
                                    for free_lines in self.relevant_free_lines_in_rows.values()])
            if free_lines_count > ship_count:
                pass
            elif free_lines_count == ship_count:
                for free_lines in self.relevant_free_lines_in_columns.values():
                    if max_length_free_line in free_lines:
                        grid_state.place_ships({max_ship_length: free_lines[max_length_free_line]})
                for free_lines in self.relevant_free_lines_in_rows.values():
                    if max_length_free_line in free_lines:
                        grid_state.place_ships({max_ship_length: free_lines[max_length_free_line]})
            else:
                raise ImpossiblePuzzleException('Not enough free lines for left ships!')

    def prepare(self, grid_state: PuzzleState):
        self.relevant_free_lines_in_rows = {}
        self.relevant_free_lines_in_columns = {}
        max_missing_ship_length = max(grid_state.missing_ships.keys())
        for row, missing_ships in enumerate(grid_state.currently_missing_ships_in_rows):
            if missing_ships < max_missing_ship_length or row not in grid_state.currently_free_lines_in_rows \
                    or max(grid_state.currently_free_lines_in_rows[row].keys()) < max_missing_ship_length:
                continue
            self.relevant_free_lines_in_rows[row] = grid_state.currently_free_lines_in_rows[row]
        for column, missing_ships in enumerate(grid_state.currently_missing_ships_in_columns):
            if missing_ships < max_missing_ship_length or column not in grid_state.currently_free_lines_in_columns \
                    or max(grid_state.currently_free_lines_in_columns[column].keys()) < max_missing_ship_length:
                continue
            self.relevant_free_lines_in_columns[column] = grid_state.currently_free_lines_in_columns[column]
        print("Max missing ship length: " + str(max_missing_ship_length))
        print("Relevant free lines in columns: " + str(self.relevant_free_lines_in_columns))
        print("Missing ships in columns: " + str(grid_state.currently_missing_ships_in_columns))
        print("Relevant free lines in rows: " + str(self.relevant_free_lines_in_rows))
        print("Missing ships in rows: " + str(grid_state.currently_missing_ships_in_rows))
