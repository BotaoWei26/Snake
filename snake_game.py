from posn import Posn
from copy import copy
from random import randint

DIRECTIONS = {
    "u": tuple((-1, 0)),
    "r": tuple((0, 1)),
    "d": tuple((1, 0)),
    "l": tuple((0, -1))
}

def same_direction(dir1, dir2):
    horz = ["r", "l"]
    vert = ["u", "d"]
    return (dir1 in horz) != (dir2 in vert)


class SnakeGame:
    def __init__(self, size):
        self.size = size
        self.board = [["+" for _ in range(self.size)] for _ in range(self.size)]
        self.head = Posn(3, 3)
        self.food = Posn(randint(0, self.size-1), randint(0,self.size-1))
        self.body = []
        self.direction = "r"
        self.game_over = False
        self._set_snake()

    def _clear_board(self):
        self.board = [["+" for _ in range(self.size)] for _ in range(self.size)]

    def _set_board(self, p, s):
        self.board[p.row][p.col] = s

    def _get_board(self, p):
        return self.board[p.row][p.col]

    def _check_off(self, p):
        return not (0 <= p.row < self.size) or not (0 <= p.col < self.size )

    def _set_snake(self):
        self._clear_board()
        self._set_board(self.head, "S")
        for seg in self.body:
            self._set_board(seg, "s")
        self._set_board(self.food, "F")

    def _place_food(self):
        while True:
            self.food = Posn(randint(0, self.size - 1), randint(0, self.size - 1))
            if self._get_board(self.food) == "+":
                break

    def move_snake(self):
        self.body.insert(0, copy(self.head))
        snake_end = self.body.pop()

        self.head += DIRECTIONS[self.direction]
        if self._check_off(self.head):
            self.game_over = True
            return

        hit_food = (self._get_board(self.head) == "F")
        hit_body = (self._get_board(self.head) == "s")

        if hit_food:
            self.body.append(snake_end)
            self._place_food()

        if hit_body:
            self.game_over = True

        self._set_snake()

    def change_direction(self, direction):
        if not same_direction(self.direction, direction):
            self.direction = direction

    def pretty_print(self):
        if self.game_over:
            print("Game Over")
            return

        for row in self.board:
            for cell in row:
                print(cell, end="")
            print()
