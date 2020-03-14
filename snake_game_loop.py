from snake_game import SnakeGame
from posn import Posn


class SnakeGameLoop(SnakeGame):
    def __init__(self, size):
        super().__init__(size)

    def _check_off(self, p):
        if super()._check_off(p):
            p %= tuple((self.size, self.size))
        return False
