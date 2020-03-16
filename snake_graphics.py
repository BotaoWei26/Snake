import tkinter as tk
from snake_game import SnakeGame, SYMBOLS, DIRECTION_KEYS
from snake_game_loop import SnakeGameLoop
from math import ceil
from dec import timeit

TICK_TIME = 75
SIZE = 25
TILE_SIZE = ceil(600 / SIZE)

SYMBOLS_COLORS = {
    SYMBOLS["empty"]: "white",
    SYMBOLS["food"]: "red",
    SYMBOLS["head"]: "dark green",
    SYMBOLS["body"]: "green"
}


class SnakeGraphics:
    def __init__(self, window, size=SIZE):
        self.window = window
        self.size = size
        self.window.title("Snake")
        self.window.geometry(str(TILE_SIZE * self.size) + "x" + str(TILE_SIZE * self.size))
        self.canvas = tk.Canvas(self.window, width=TILE_SIZE * self.size, height=TILE_SIZE * self.size)
        self.canvas.pack()
        self.window.bind("<Key>", self._key_input)
        self._reset()

    def _reset(self):
        self.game = SnakeGameLoop(self.size)
        self.board_memory = self.game.get_board()
        self._draw_board()
        self.window.after(TICK_TIME, self._tick)
        self.game_over = False
        self._set_board()

    def _set_board(self):
        self.board_rectangles = []
        board = self.game.get_board()
        for i, row in enumerate(board):
            rectangles_row = []
            for j, cell in enumerate(row):
                rectangles_row.append(self.canvas.create_rectangle(TILE_SIZE * j, TILE_SIZE * i,
                                                                   TILE_SIZE * (j + 1), TILE_SIZE * (i + 1),
                                                                   fill=SYMBOLS_COLORS[cell]))
            self.board_rectangles.append(rectangles_row)

    def _draw_board(self):
        board = self.game.get_board()
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if self.board_memory[i][j] != cell:
                    self.canvas.itemconfig(self.board_rectangles[i][j], fill=SYMBOLS_COLORS[cell])
        self.board_memory = board

    def _tick(self):
        self.game.move_snake()
        self._draw_board()
        if not self._check_gameover():
            self.window.after(TICK_TIME, self._tick)
        else:
            self.game_over = True

    def _key_input(self, event):
        if self.game_over:
            self._reset()
        elif event.char in DIRECTION_KEYS.values():
            self.game.change_direction(event.char)

    def _check_gameover(self):
        return self.game.game_over


