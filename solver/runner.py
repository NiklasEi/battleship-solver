import time
from typing import List

from puzzle_state import PuzzleState
from steps.step import Step


class Runner:
    """
    This class contains a list with logic steps that can be subsequently executed.
    """
    debug = True
    steps: List[Step] = []

    def add_step(self, step: Step):
        self.steps.append(step)

    def run(self, grid_state: PuzzleState):
        for step in self.steps:
            step.prepare(grid_state)
            if self.debug:
                time_start = time.time()
                print("Running step " + str(step.__class__.__name__) + ": Changes? "
                      + str(step.check_for_next_step(grid_state)))
                if step.check_for_next_step(grid_state):
                    step.do_next_step(grid_state)
                    grid_state.display()
                    print("Took " + str(time.time() - time_start) + " seconds")
            elif step.check_for_next_step(grid_state):
                step.do_next_step(grid_state)
