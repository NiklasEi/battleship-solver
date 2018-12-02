from enum import Enum, unique


@unique
class PuzzleParam(Enum):
    """
    Enum representing keys for puzzle parameters.
    Hide magic values for serialization and deserialization.
    """
    ROWS = " "
    SHIP = "O"
    BLOCKED = "X"