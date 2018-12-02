from abc import ABC, abstractmethod
from puzzle_state import PuzzleState


class Step(ABC):
    """
    Base class for logic steps
    """
    @abstractmethod
    def check_for_next_step(self, grid_state: PuzzleState) -> bool:
        return False

    @abstractmethod
    def do_next_step(self, grid_state: PuzzleState):
        pass

    def prepare(self, grid_state: PuzzleState):
        pass
