class Posn:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __add__(self, other):
        return Posn(self.row + other[0], self.col + other[1])

    def __iadd__(self, other):
        self.row += other[0]
        self.col += other[1]
        return self

    def __imod__(self, other):
        self.row %= other[0]
        self.col %= other[1]
        return self
