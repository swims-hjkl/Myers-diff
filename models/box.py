
class Box:

    def __init__(self, left, top, right, bottom):
        self.top = top
        self.left = left
        self.bottom = bottom
        self.right = right
        self.height = bottom - top
        self.width = right - left
        self.size = self.height + self.width
        self.delta = self.width - self.height

    def __repr__(self):
        return f'Box<{self.left}, {self.top}, {self.right}, {self.bottom}>'
