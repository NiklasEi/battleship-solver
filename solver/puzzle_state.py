from typing import List, Dict

import numpy as np
from enums.slot_state import SlotState


class PuzzleState:
    """
    Represents a state of a puzzle.
    This includes a given grid with certain dimensions and ships,
    but also the current state of the solving process.
    """

    def __init__(self, puzzle, ships, initial_state: List[str] = None):
        self.puzzle = puzzle
        self.ships: Dict[int, int] = ships
        self.current_counts_columns = np.zeros(self.puzzle.columns, dtype=int)
        self.current_counts_rows = np.zeros(self.puzzle.rows, dtype=int)
        self.state = np.full((self.puzzle.columns, self.puzzle.rows), SlotState.EMPTY.value)
        self.missing_ships: Dict[int, int] = {}
        self.free_lines = {}
        self.placed_ships = {}
        self.currently_free_lines_in_columns: Dict[int, Dict[int, List[List[List[int]]]]] = {}
        self.currently_free_lines_in_rows: Dict[int, Dict[int, List[List[List[int]]]]] = {}
        self.currently_missing_ships_in_columns: List[int] = []
        self.currently_missing_ships_in_rows: List[int] = []
        self.calculate_missing_ships()
        self.update_free_lines()
        if initial_state is not None:
            print("loading initial state...")
            for row, states_string in enumerate(initial_state):
                for column, state_string in enumerate(list(states_string)):
                    self.place_single_slot_state(column, row, SlotState(state_string))
            self.calculate_missing_ships()
            self.update_free_lines()
        print("Ships: " + str(self.ships) + "   Left ships: " + str(self.missing_ships))
        print("Placed: " + str(self.placed_ships))
        print("Current GridState:")
        self.display()

    def display(self):
        for row in range(self.puzzle.rows):
            for column in range(self.puzzle.columns):
                print("+---", end='')
            print("+")
            print("| ", end='')
            for column in range(self.puzzle.columns):
                print(self.state[column][row] + " | ", end='')
            print(" " + str(self.current_counts_rows[row]) + "/" + str(self.puzzle.counts_rows[row]))

        for column in range(self.puzzle.columns):
            print("+---", end='')
        print("+")

        for column in range(self.puzzle.columns):
            print(" " + str(self.current_counts_columns[column])
                  + "/" + str(self.puzzle.counts_columns[column]), end='')
        print()

    def place_ships(self, ships_to_add):
        print("Placing ships: " + str(ships_to_add))
        for ship_length, ship_positions in ships_to_add.items():
            for ship_position in ship_positions:
                for coordinate in ship_position:
                    if self.state[coordinate[0]][coordinate[1]] != SlotState.EMPTY.value:
                        print("Unexpected value in slot! Should be empty, found: "
                              + SlotState(self.state[coordinate[0]][coordinate[1]]).name + "; Skipping slot!")
                        continue
                    self.state[coordinate[0]][coordinate[1]] = SlotState.SHIP.value
                    self.current_counts_columns[coordinate[0]] += 1
                    self.current_counts_rows[coordinate[1]] += 1
                self.placed_ships.setdefault(ship_length, []).append(ship_position)
                if self.missing_ships[ship_length] == 1:
                    self.missing_ships.pop(ship_length)
                else:
                    self.missing_ships[ship_length] = self.missing_ships.pop(ship_length) - 1
                for column, row in self.puzzle.get_surrounding_slots(ship_position):
                    self.state[column][row] = SlotState.WATER.value

    def update(self):
        self.calculate_missing_ships()
        self.update_free_lines()

    def update_free_lines(self):
        self.currently_free_lines_in_rows: Dict[int, Dict[int, List[List[List[int]]]]] = {}
        for column in range(self.puzzle.columns):
            self.currently_free_lines_in_columns[column] = self.get_free_lines({"columns": [column]})
        for row in range(self.puzzle.rows):
            self.currently_free_lines_in_rows[row] = self.get_free_lines({"rows": [row]})
        self.free_lines: Dict[int, List[List[List[int]]]] = {}
        for row_dict in self.currently_free_lines_in_rows.values():
            for line_length, lines in row_dict.items():
                self.free_lines.setdefault(line_length, []).extend(lines)
        for column_dict in self.currently_free_lines_in_columns.values():
            for line_length, lines in column_dict.items():
                self.free_lines.setdefault(line_length, []).extend(lines)

    def calculate_missing_ships(self):
        self.missing_ships: Dict[int, int] = {}
        for ship_length, ship_count in self.ships.items():
            placed_ships_of_length = 0 if ship_length not in self.placed_ships else len(self.placed_ships[ship_length])
            if placed_ships_of_length < ship_count:
                self.missing_ships[ship_length] = ship_count - placed_ships_of_length
            elif placed_ships_of_length == ship_count:
                continue
            else:
                raise ValueError('More ships placed of length ' + str(ship_length) + " then there are in puzzle!"
                                 + str(placed_ships_of_length) + "/" + str(ship_count))
        self.currently_missing_ships_in_columns \
            = [count - placed for (count, placed)
               in zip(self.puzzle.counts_columns, self.current_counts_columns)]
        self.currently_missing_ships_in_rows \
            = [count - placed for (count, placed)
               in zip(self.puzzle.counts_rows, self.current_counts_rows)]

    def get_free_lines(self, columns_and_rows: Dict[str, List[int]]) -> Dict[int, List[List[List[int]]]]:
        free_lines: Dict[int, List[List[List[int]]]] = {}
        key_rows = "rows"
        key_columns = "columns"
        if key_rows in columns_and_rows:
            for row in columns_and_rows[key_rows]:
                consecutive_free_slots = 0
                current_slots: List[List[int]] = []
                for column in range(self.puzzle.columns):
                    if self.state[column][row] == SlotState.WATER.value:
                        if consecutive_free_slots > 0:
                            free_lines.setdefault(consecutive_free_slots, []).append(current_slots)
                            consecutive_free_slots = 0
                            current_slots = []
                            continue
                    elif consecutive_free_slots > 0 or self.state[column][row] == SlotState.EMPTY.value \
                            or self.state[column][row] == SlotState.SHIP_WEST.value:
                        current_slots.append([column, row])
                        consecutive_free_slots += 1
                if consecutive_free_slots > 0:
                    free_lines.setdefault(consecutive_free_slots, []).append(current_slots)

        if key_columns in columns_and_rows:
            for column in columns_and_rows[key_columns]:
                consecutive_free_slots = 0
                current_slots = []
                for row in range(self.puzzle.rows):
                    if self.state[column][row] == SlotState.WATER.value:
                        if consecutive_free_slots > 0:
                            free_lines.setdefault(consecutive_free_slots, []).append(current_slots)
                            consecutive_free_slots = 0
                            current_slots = []
                            continue
                    elif consecutive_free_slots > 0 or self.state[column][row] == SlotState.EMPTY.value \
                            or self.state[column][row] == SlotState.SHIP_NORTH.value:
                        current_slots.append([column, row])
                        consecutive_free_slots += 1
                if consecutive_free_slots > 0:
                    free_lines.setdefault(consecutive_free_slots, []).append(current_slots)

        return free_lines

    def place_single_slot_state(self, column, row, slot_state: SlotState):
        print("placing " + slot_state.value + " in " + str(column) + "/" + str(row))
        if slot_state is SlotState.EMPTY:
            return
        self.state[column][row] = slot_state.value
        if slot_state is SlotState.WATER:
            return
        self.current_counts_columns[column] += 1
        self.current_counts_rows[row] += 1
        surrounding_water = self.puzzle.get_surrounding_slots([[column, row]], slot_state=slot_state)
        for coordinate in surrounding_water:
            self.state[coordinate[0]][coordinate[1]] = SlotState.WATER.value
        if slot_state is SlotState.SHIP_SINGLE:
            self.placed_ships.setdefault(1, []).append([[column, row]])
            if self.missing_ships[1] == 1:
                self.missing_ships.pop(1)
            else:
                self.missing_ships[1] = self.missing_ships.pop(1) - 1
        elif slot_state is not SlotState.SHIP:
            # get the slot next to the ship ending and place a ship there
            for column, row in self.puzzle.get_surrounding_slots([[column, row]]):
                if [column, row] in surrounding_water:
                    continue
                self.place_single_slot_state(column, row, slot_state=SlotState.SHIP)
                break
