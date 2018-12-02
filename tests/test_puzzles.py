import os
import unittest
import json
from solver.solver import BattleShipSolver
from typing import Dict
from unittest import TestCase


class TestPuzzles(TestCase):
    """
    Test the solver on a collection of puzzles
    """
    def setUp(self):
        """
        Load the json file with the test puzzles
        :return:
        """
        with open("resources" + os.sep + "test_puzzles.json") as json_data:
            self.puzzle_json = json.load(json_data)
            print("loaded " + str(self.puzzle_json))

    def test_puzzles(self):
        for count, puzzle_json_dict in enumerate(self.puzzle_json["puzzles"]):
            puzzle = self.load_puzzle_data(puzzle_json_dict)
            current_solver = BattleShipSolver(puzzle["columns"], puzzle["rows"], puzzle["ships"]
                                              , puzzle["counts_columns"], puzzle["counts_rows"])
            current_solver.start()
            print("Puzzle " + str(count))
            del current_solver

    @staticmethod
    def load_puzzle_data(puzzle_dict) -> Dict:
        """
        Prepare the dictionary from json data for direct use in the solver

        :param puzzle_dict: dictionary loaded from the json file
        :return: dictionary with correctly formatted values for use in the solver
        """
        puzzle_dict["ships"] = {int(key): val for key, val in puzzle_dict["ships"].items()}
        return puzzle_dict


if __name__ == '__main__':
    unittest.main()
