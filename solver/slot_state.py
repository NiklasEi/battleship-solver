from enum import Enum, unique


@unique
class SlotState(Enum):
    EMPTY = " "
    SHIP = "O"
    BLOCKED = "X"
