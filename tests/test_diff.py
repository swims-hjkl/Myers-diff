import unittest

from myers_diff import Diff, Box


class TestDiff(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("tests/data/from_diff.txt", "r") as f:
            cls._from_diff = f.read().splitlines()
        with open("tests/data/to_diff.txt", "r") as f:
            cls._to_diff = f.read().splitlines()
        cls._diff = Diff(cls._from_diff, cls._to_diff)

    def test_midpoint(self):
        box = Box(0, 0, len(self._from_diff) - 1, len(self._to_diff) - 1)
        self.assertEqual(self._diff.midpoint(box), ((6, 5), (9, 7)))
        box = Box(0, 0, 3, 2)
        self.assertEqual(self._diff.midpoint(box), ((1, 0), (2, 2)))

    def test_find_path(self):
        expected = [(0, 0), (1, 0), (2, 2), (3, 2), (4, 2), (5, 4), (6, 4),
                    (6, 5), (9, 7), (10, 9), (11, 9), (11, 10), (11, 11),
                    (12, 12), (13, 12), (13, 13), (14, 14)]
        actual = self._diff.find_path(
            0, 0, len(self._from_diff), len(self._to_diff))
        self.assertEqual(expected, actual)

    def test_walk_snakes(self):
        expected = [(0, 0), (1, 0), (2, 2), (3, 2), (4, 2), (5, 4), (6, 4),
                    (6, 5), (9, 7), (10, 9), (11, 9), (11, 10), (11, 11),
                    (12, 12), (13, 12), (13, 13), (14, 14)]
        actual = self._diff.find_path(
            0, 0, len(self._from_diff), len(self._to_diff))
        self.assertEqual(expected, actual)
