from grid_state import GridState
from impossible_puzzle_exception import ImpossiblePuzzleException
from steps.step import Step


class PlaceLongestShips(Step):

    def check_for_next_step(self, grid_state: GridState):
        max_ship_length = max(grid_state.left_ships.keys())
        print(str(grid_state.free_lines))
        max_length_free_line = max(grid_state.free_lines.keys())
        if max_length_free_line == max_ship_length:
            ship_count = grid_state.left_ships[max_ship_length]
            free_lines_count = len(grid_state.free_lines[max_length_free_line])
            if free_lines_count == ship_count:
                return True
        return False

    def do_next_step(self, grid_state: GridState):
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

    def prepare(self, grid_state: GridState):
        grid_state.update_free_lines()
