import unittest

from myers_diff import Box


class TestBox(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._box = Box(5, 4, 12, 12)

    def test_height(self):
        self.assertEqual(
            8,
            self._box.height
        )

    def test_width(self):
        self.assertEqual(
            7,
            self._box.width
        )

    def test_size(self):
        self.assertEqual(
            15,
            self._box.size
        )

    def test_delta(self):
        self.assertEqual(
            -1,
            self._box.delta
        )
