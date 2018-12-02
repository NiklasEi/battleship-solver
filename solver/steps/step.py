from abc import ABC, abstractmethod
from grid_state import GridState


class Step(ABC):
    """
    Base class for logic steps
    """
    @abstractmethod
    def check_for_next_step(self, grid_state: GridState) -> bool:
        return False

    @abstractmethod
    def do_next_step(self, grid_state: GridState):
        pass

    def prepare(self, grid_state: GridState):
        pass
