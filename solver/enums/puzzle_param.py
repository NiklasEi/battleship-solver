from enum import Enum, unique


@unique
class PuzzleParam(Enum):
    """
    Enum representing keys for puzzle parameters.
    Hide magic values for serialization and deserialization.
    """
    ROWS = "rows"
    COLUMNS = "columns"
    SHIPS = "ships"
    COUNTS_COLUMNS = "counts_columns"
    COUNTS_ROWS = "counts_rows"
