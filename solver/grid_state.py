from typing import List, Dict

import numpy as np
from solver.slot_state import SlotState


class GridState:
    def __init__(self, grid=None, ships=None, placed_ships={}, origin=None):
        if origin is None:
            assert grid is not None and ships is not None, \
                "Either give original GridState or the grid and ships"
            self.grid = grid
            self.ships: Dict[int, int] = ships
            self.placed_ships = placed_ships
            self.left_ships: Dict[int, int] = {}
            self.free_lines = {}
            self.current_counts_columns = np.zeros(self.grid.columns, dtype=int)
            self.current_counts_rows = np.zeros(self.grid.rows, dtype=int)
            self.state = np.full((self.grid.columns, self.grid.rows), SlotState.EMPTY.value)
            self.place_ships(placed_ships)
        else:
            assert grid is None and ships is None, \
                "Grid and ships are ignored because of passed original GridState"
            # ToDo
        self.calculate_left_ships()
        print("Ships: " + str(self.ships) + "   Left ships: " + str(self.left_ships))
        print("Placed: " + str(self.placed_ships))
        self.update_free_lines()
        print("Current GridState:")
        self.display()

    def display(self):
        for row in range(self.grid.rows):
            for column in range(self.grid.columns):
                print("+---", end='')
            print("+")
            print("| ", end='')
            for column in range(self.grid.columns):
                print(self.state[column][row] + " | ", end='')
            print(" " + str(self.current_counts_rows[row]) + "/" + str(self.grid.counts_rows[row]))

        for column in range(self.grid.columns):
            print("+---", end='')
        print("+")

        for column in range(self.grid.columns):
            print(" " + str(self.current_counts_columns[column])
                  + "/" + str(self.grid.counts_columns[column]), end='')
        print()

    def place_ships(self, ships_to_add):
        for ship_length, ship_positions in ships_to_add.items():
            for ship_position in ship_positions:
                for coordinate in ship_position:
                    if self.state[coordinate[0]][coordinate[1]] != SlotState.EMPTY.value:
                        print("Unexpected value in slot! Should be empty, found: "
                              + SlotState(self.state[coordinate[0]][coordinate[1]]).name + "; Overwriting with ship!")
                    self.state[coordinate[0]][coordinate[1]] = SlotState.SHIP.value
                    self.current_counts_columns[coordinate[0]] += 1
                    self.current_counts_rows[coordinate[1]] += 1
                self.placed_ships.setdefault(ship_length, []).append(ship_position)
                if self.left_ships[ship_length] == 1:
                    self.left_ships.pop(ship_length)
                else:
                    self.left_ships[ship_length] = self.left_ships.pop(ship_length) - 1
                # ToDo: get surrounding slots of ship and block them!

    def update_free_lines(self):
        self.free_lines = {}
        for column in range(self.grid.columns):
            consecutive_free_slots = 0
            current_slots = []
            for row in range(self.grid.rows):
                if self.state[column][row] != SlotState.EMPTY.value:
                    if consecutive_free_slots > 0:
                        self.free_lines.setdefault(consecutive_free_slots, []).append(current_slots)
                        consecutive_free_slots = 0
                        current_slots = []
                        continue
                else:
                    current_slots.append([column, row])
                    consecutive_free_slots += 1

            if consecutive_free_slots > 0:
                self.free_lines.setdefault(consecutive_free_slots, []).append(current_slots)
        for row in range(self.grid.rows):
            consecutive_free_slots = 0
            current_slots = []
            for column in range(self.grid.columns):
                if self.state[column][row] != SlotState.EMPTY.value:
                    if consecutive_free_slots > 0:
                        self.free_lines.setdefault(consecutive_free_slots, []).append(current_slots)
                        consecutive_free_slots = 0
                        current_slots = []
                        continue
                else:
                    current_slots.append([column, row])
                    consecutive_free_slots += 1

            if consecutive_free_slots > 0:
                self.free_lines.setdefault(consecutive_free_slots, []).append(current_slots)

    def get_surrounding_slots(self, slots: List[List[int]]):
        # ToDo
        pass

    def calculate_left_ships(self):
        self.left_ships: Dict[int, int] = {}
        for ship_length, ship_count in self.ships.items():
            print("Ships: " + str(self.ships) + "   current: " + str(ship_length) + ": " + str(ship_count))
            placed_ships_of_length = 0 if ship_length not in self.placed_ships else len(self.placed_ships[ship_length])
            if placed_ships_of_length < ship_count:
                self.left_ships[ship_length] = ship_count - placed_ships_of_length
            elif placed_ships_of_length == ship_count:
                continue
            else:
                raise ValueError('More ships placed of length ' + str(ship_length) + " then there are in puzzle!"
                                 + str(placed_ships_of_length) + "/" + str(ship_count))
