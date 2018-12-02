from puzzle_state import PuzzleState
from impossible_puzzle_exception import ImpossiblePuzzleException
from steps.step import Step


class PlaceLongestShips(Step):
    """
    Checks whether there are only as many possible lines left for the
    longest ship, as there are ships left to place for that length.
    """

    def check_for_next_step(self, grid_state: PuzzleState):
        max_ship_length = max(grid_state.left_ships.keys())
        print(str(grid_state.free_lines))
        max_length_free_line = max(grid_state.free_lines.keys())
        if max_length_free_line == max_ship_length:
            ship_count = grid_state.left_ships[max_ship_length]
            free_lines_count = len(grid_state.free_lines[max_length_free_line])
            print("counts (ships): " + str(ship_count) + "  and (lines): " + str(free_lines_count))
            if free_lines_count == ship_count:
                return True
        print("max ship length: " + str(max_ship_length) + "  max free line: " + str(max_length_free_line))
        print("Ship keys: " + str(grid_state.left_ships.keys()))
        return False

    def do_next_step(self, grid_state: PuzzleState):
        max_ship_length = max(grid_state.left_ships.keys())
        max_length_free_line = max(grid_state.free_lines.keys())
        if max_length_free_line == max_ship_length:
            ship_count = grid_state.left_ships[max_ship_length]
            free_lines_count = len(grid_state.free_lines[max_length_free_line])
            if free_lines_count > ship_count:
                pass
            elif free_lines_count == ship_count:
                grid_state.place_ships({max_ship_length: grid_state.free_lines[max_length_free_line]})
            else:
                raise ImpossiblePuzzleException('Not enough free lines for left ships!')

    def prepare(self, grid_state: PuzzleState):
        grid_state.update_free_lines()
