import numpy as np
from solver.slot_state import SlotState


class GridState:
    def __init__(self, grid=None, ships=None, placed_ships={}, origin=None):
        if origin is None:
            assert grid is not None and ships is not None, \
                "Either give original GridState or the grid and ships"
            self.grid = grid
            self.ships = ships
            self.placed_ships = placed_ships
            self.current_counts_columns = np.zeros(self.grid.columns, dtype=int)
            self.current_counts_rows = np.zeros(self.grid.rows, dtype=int)
            self.state = np.full((self.grid.columns, self.grid.rows), SlotState.EMPTY.value)
            self.place_ships(placed_ships)
        else:
            assert grid is None and ships is None, \
                "Grid and ships are ignored because of passed original GridState"
        self.check_and_make_trivial_placements()
        print("Final stage of current GridState:")
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

    def resolve_trivial_counts(self):
        for row, count in enumerate(self.grid.counts_rows):
            if count == self.grid.columns:
                ship_position = []
                for column in range(self.grid.columns):
                    ship_position.append([column, row])
                self.place_ships({self.grid.columns: [ship_position]})
        for column, count in enumerate(self.grid.counts_columns):
            if count == self.grid.rows:
                ship_position = []
                for row in range(self.grid.rows):
                    ship_position.append([column, row])
                self.place_ships({self.grid.rows: [ship_position]})

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

    def check_and_make_trivial_placements(self):
        self.resolve_trivial_counts()
        self.block_rows_with_all_ships_set()
        self.block_columns_with_all_ships_set()

    def block_rows_with_all_ships_set(self):
        for row, count in enumerate(self.grid.counts_rows):
            if count == self.current_counts_rows[row]:
                for column in range(self.grid.columns):
                    if self.state[column][row] == SlotState.EMPTY.value:
                        self.state[column][row] = SlotState.BLOCKED.value

    def block_columns_with_all_ships_set(self):
        for column, count in enumerate(self.grid.counts_columns):
            if count == self.current_counts_columns[column]:
                for row in range(self.grid.rows):
                    if self.state[column][row] == SlotState.EMPTY.value:
                        self.state[column][row] = SlotState.BLOCKED.value