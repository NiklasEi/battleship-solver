from enum import Enum, unique


@unique
class SlotState(Enum):
    """
    Enum representing different states a grid slot can have.
    The values are also used when reading in puzzles.
    """
    EMPTY = " "
    SHIP = "O"
    BLOCKED = "X"
