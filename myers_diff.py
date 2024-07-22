# Space optimized algorithm for myers_diff
import math

from models.box import Box
from models.diff import DiffType, DiffDescriptor
import utils


class Diff:

    def __init__(self, from_diff, to_diff):
        self.a = from_diff
        self.b = to_diff

    def find_path(self, left, top, right, bottom):
        box = Box(left, top, right, bottom)
        snake = self.midpoint(box)
        if not snake:
            return

        start, finish = snake
        head = self.find_path(box.left, box.top, start[0], start[1])
        tail = self.find_path(finish[0], finish[1], box.right, box.bottom)

        return (head or [start]) + (tail or [finish])

    def midpoint(self, box: Box):
        if box.size == 0:
            return

        max = math.ceil(box.size / 2)

        vf = [None for i in range(0, (2 * max) + 1)]
        vf[1] = box.left
        vb = [None for i in range(0, (2 * max) + 1)]
        vb[1] = box.bottom

        for d in range(0, max + 1):
            snake = self.forward(box, d, vf, vb)
            if snake:
                return snake
            snake = self.backward(box, d, vf, vb)
            if snake:
                return snake

    def forward(self, box, d, vf, vb):
        for k in range(d, -d - 1, -2):

            c = k - box.delta

            if k == -d or (k != d and vf[k - 1] < vf[k + 1]):
                px = x = vf[k+1]
            else:
                px = vf[k - 1]
                x = px + 1
            y = box.top + (x - box.left) - k
            py = y if (d == 0 or x != px) else y - 1

            while x < box.right and y < box.bottom and self.a[x] == self.b[y]:
                x, y = x + 1, y + 1

            vf[k] = x

            if c > (len(vb) - 1) or vb[c] is None:
                continue

            if box.delta % 2 != 0 and y >= vb[c]:
                # the next line will at least prevent overlap at 0
                if -(d - 1) <= c and c <= d - 1:
                    return ((px, py), (x, y))

    def backward(self, box, d, vf, vb):
        for c in range(d, -d - 1, -2):

            k = c + box.delta

            if c == -d or (c != d and vb[c - 1] > vb[c+1]):
                py = y = vb[c+1]
            else:
                py = vb[c - 1]
                y = py - 1

            x = box.left + (y - box.top) + k
            px = x if (d == 0 or y != py) else x + 1

            while x > box.left and y > box.top and self.a[x - 1] == self.b[y-1]:
                x, y = x - 1, y - 1

            vb[c] = y

            if k > (len(vf) - 1) or vf[k] is None:
                continue

            if box.delta % 2 == 0 and x <= vf[k]:
                # the next line will at least prevent overlap at 0
                if -d <= k and k <= d:
                    return ((x, y), (px, py))

    def walk_diagonal(self, x1, y1, x2, y2):
        while x1 < x2 and y1 < y2 and self.a[x1] == self.b[y1]:
            yield (x1, y1, x1 + 1, y1 + 1)
            x1, y1 = x1 + 1, y1 + 1
        yield (x1, y1)

    def _get_equality(self, x1, y1, x2, y2):
        if (x2 - x1) == (y2 - y1):
            return 0
        elif (x2 - x1) > (y2 - y1):
            return 1
        else:
            return -1

    def walk_snakes(self):
        path = self.find_path(0, 0, len(self.a) - 1, len(self.b) - 1)

        if not path:
            return

        for (x1, y1), (x2, y2) in utils.pairwise(path):
            for diagonal_traverse_result in self.walk_diagonal(x1, y1, x2, y2):
                if len(diagonal_traverse_result) > 2:
                    xd1, yd1, xd2, yd2 = diagonal_traverse_result
                    yield xd1, yd1, xd2, yd2
                else:
                    x1, y1 = diagonal_traverse_result

            _direction = self._get_equality(x1, y1, x2, y2)
            if _direction == -1:
                yield x1, y1, x1, y1 + 1
                y1 += 1
            elif _direction == 1:
                yield x1, y1, x1 + 1, y1
                x1 += 1

            for diagonal_traverse_result in self.walk_diagonal(x1, y1, x2, y2):
                if len(diagonal_traverse_result) > 2:
                    xd1, yd1, xd2, yd2 = diagonal_traverse_result
                    yield xd1, yd1, xd2, yd2

    def diff(self):

        for x1, y1, x2, y2 in self.walk_snakes():
            if x1 == x2:
                yield DiffDescriptor(DiffType.INSERTED, None, y1)
            elif y1 == y2:
                yield DiffDescriptor(DiffType.DELETED, x1, None)
            else:
                yield DiffDescriptor(DiffType.EQUALS, x1, y1)


if __name__ == "__main__":
    with open("tests/data/wrong.txt", "r") as f:
        _from_diff = f.read().split("\n")
    with open("tests/data/to_diff.txt", "r") as f:
        _to_diff = f.read().split("\n")
    print(_to_diff)
    _diff = Diff(_from_diff, _to_diff)

    new_diff = []
    for k in _diff.diff():
        if k.diff_type == DiffType.INSERTED:
            new_diff.append(_to_diff[k.to_index])
        if k.diff_type == DiffType.EQUALS:
            new_diff.append(_to_diff[k.to_index])

    print("\n".join(new_diff))
