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
            if grid_state.puzzle.is_solved():
                return
            step.prepare(grid_state)
            if self.debug:
                time_start = time.time()
                check_for_next_step = step.check_for_next_step(grid_state)
                print("Running step " + str(step.__class__.__name__) + ": Changes? "
                      + str(check_for_next_step))
                if check_for_next_step:
                    step.do_next_step(grid_state)
                    grid_state.update()
                    grid_state.display()
                    print("Took " + str(time.time() - time_start) + " seconds")
            elif step.check_for_next_step(grid_state):
                step.do_next_step(grid_state)
