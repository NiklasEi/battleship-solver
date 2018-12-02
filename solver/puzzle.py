from typing import Dict, List

from enums.puzzle_param import PuzzleParam
from enums.slot_state import SlotState
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
        if PuzzleParam.INITIAL_STATE.value in puzzle:
            print("Found initial state " + str(puzzle[PuzzleParam.INITIAL_STATE.value]))
            self.initial_state = PuzzleState(self, self.ships, initial_state=puzzle[PuzzleParam.INITIAL_STATE.value])
        else:
            self.initial_state = PuzzleState(self, self.ships)
        self.current_state = self.initial_state

    def is_solved(self) -> bool:
        # ToDo: when getting to have to guess possible solutions one needs more then one state here
        #    For now just return, whether there are ships left to place
        return not any(self.current_state.left_ships)

    def get_surrounding_slots(self, slots: List[List[int]], slot_state: SlotState=None) -> List[List[int]]:
        """
        Get surrounding slots of given slots
        :return list containing surrounding coordinates
        """
        surrounding_slots = set()
        print("calc surrounding for " + str(slots))
        for column, row in slots:
            if column > 0:
                if slot_state is not SlotState.SHIP and slot_state is not SlotState.SHIP_EAST:
                    surrounding_slots.add((column-1, row))
                if row > 0:
                    surrounding_slots.add((column-1, row-1))
                if row < self.rows - 1:
                    surrounding_slots.add((column-1, row+1))
            if column < self.columns - 1:
                if slot_state is not SlotState.SHIP and slot_state is not SlotState.SHIP_WEST:
                    surrounding_slots.add((column + 1, row))
                if row > 0:
                    surrounding_slots.add((column + 1, row - 1))
                if row < self.rows - 1:
                    surrounding_slots.add((column + 1, row + 1))
            if row > 0 and slot_state is not SlotState.SHIP and slot_state is not SlotState.SHIP_SOUTH:
                surrounding_slots.add((column, row - 1))
            if row < self.rows - 1 and slot_state is not SlotState.SHIP and slot_state is not SlotState.SHIP_NORTH:
                surrounding_slots.add((column, row + 1))
        to_return = [[column, row] for column, row in surrounding_slots]
        for slot in slots:
            if slot in to_return:
                to_return.remove(slot)
        return to_return
