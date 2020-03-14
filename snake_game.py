from posn import Posn
from copy import copy
from random import randint

DIRECTION_KEYS = {
    "RIGHT": "d",
    "LEFT": "a",
    "UP": "w",
    "DOWN": "s"
}

DIRECTIONS = {
    DIRECTION_KEYS["UP"]: tuple((-1, 0)),
    DIRECTION_KEYS["RIGHT"]: tuple((0, 1)),
    DIRECTION_KEYS["DOWN"]: tuple((1, 0)),
    DIRECTION_KEYS["LEFT"]: tuple((0, -1))
}

SYMBOLS = {
    "empty": "+",
    "food": "f",
    "head": "S",
    "body": "s"
}


def same_direction(dir1, dir2):
    horz = [DIRECTION_KEYS["RIGHT"], DIRECTION_KEYS["LEFT"]]
    vert = [DIRECTION_KEYS["UP"], DIRECTION_KEYS["DOWN"]]
    return (dir1 in horz) != (dir2 in vert)


class SnakeGame:
    def __init__(self, size):
        self.size = size
        self.board = [[SYMBOLS["empty"] for _ in range(self.size)] for _ in range(self.size)]
        self.head = Posn(3, 3)
        self.food = Posn(randint(0, self.size-1), randint(0,self.size-1))
        self.body = []
        self.direction = DIRECTION_KEYS["RIGHT"]
        self.game_over = False
        self.turn_trigger = False
        self._set_snake()

    def _clear_board(self):
        self.board = [[SYMBOLS["empty"] for _ in range(self.size)] for _ in range(self.size)]

    def _set_board(self, p, s):
        self.board[p.row][p.col] = s

    def _get_board(self, p):
        return self.board[p.row][p.col]

    def _check_off(self, p):
        return not (0 <= p.row < self.size) or not (0 <= p.col < self.size )

    def _set_snake(self):
        self._clear_board()
        self._set_board(self.head, SYMBOLS["head"])
        for seg in self.body:
            self._set_board(seg, SYMBOLS["body"])
        self._set_board(self.food, SYMBOLS["food"])

    def _place_food(self):
        ############# redo this
        while True:
            self.food = Posn(randint(0, self.size - 1), randint(0, self.size - 1))
            if self._get_board(self.food) == SYMBOLS["empty"]:
                break

    def move_snake(self):
        self.body.insert(0, copy(self.head))
        snake_end = self.body.pop()

        self.head += DIRECTIONS[self.direction]
        if self._check_off(self.head):
            self.game_over = True
            return

        hit_food = (self._get_board(self.head) == SYMBOLS["food"])
        hit_body = (self._get_board(self.head) == SYMBOLS["body"])

        if hit_food:
            self.body.append(snake_end)
            self._place_food()

        if hit_body:
            self.game_over = True

        self._set_snake()
        self.turn_trigger = True

    def change_direction(self, direction):
        if not same_direction(self.direction, direction) and self.turn_trigger:
            self.direction = direction
            self.turn_trigger = False

    def pretty_print(self):
        if self.game_over:
            print("Game Over")
            return

        for row in self.board:
            for cell in row:
                print(cell, end="")
            print()

    def get_board(self):
        return self.board
