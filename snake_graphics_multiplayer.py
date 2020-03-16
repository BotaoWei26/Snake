from snake_graphics import SnakeGraphics, SYMBOLS_COLORS
import tkinter as tk
from snake_game import SnakeGame, SYMBOLS, DIRECTION_KEYS
from snake_game_loop import SnakeGameLoop

TICK_TIME = 75
SIZE = 10
TILE_SIZE = 10


class SnakeGraphicsMultiplayer(SnakeGraphics):
    def __init__(self, window, size=SIZE):
        self.window = window
        self.size = size
        self.window.title("Snake")
        self.window.geometry(str(TILE_SIZE * self.size * 2) + "x" + str(TILE_SIZE * self.size))
        self.canvas = tk.Canvas(self.window, width=TILE_SIZE * self.size + 100, height=TILE_SIZE * self.size,
                                bd=10, relief='solid'
                                )
        self.canvas.pack()
        self.window.bind("<Key>", self._key_input)
        self._reset()