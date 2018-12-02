from enum import Enum, unique


@unique
class SlotState(Enum):
    """
    Enum representing different states a grid slot can have.
    The values are also used when reading in puzzles.
    """
    EMPTY = " "
    SHIP = "X"  # unknown piece of ship
    WATER = "~"
    SHIP_NORTH = "n"
    SHIP_SOUTH = "s"
    SHIP_EAST = "e"
    SHIP_WEST = "w"
    SHIP_SINGLE = "o"
