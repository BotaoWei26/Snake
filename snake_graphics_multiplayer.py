from snake_graphics import SnakeGraphics, SYMBOLS_COLORS
import tkinter as tk
from snake_game import SnakeGame, SYMBOLS, DIRECTION_KEYS
from snake_game_loop import SnakeGameLoop
from math import ceil
from dec import timeit


TICK_TIME = 75
SIZE = 25
TILE_SIZE = ceil(600 / SIZE)


class SnakeGraphicsMultiplayer(SnakeGraphics):
    def __init__(self, window, size=SIZE):
        self.window = window
        self.size = size
        self.window.title("Snake")
        self.window.geometry(str(TILE_SIZE * self.size * 2 + 100) + "x" + str(TILE_SIZE * self.size + 100))

        self.canvas = tk.Canvas(self.window, width=(TILE_SIZE * self.size),
                                height=(TILE_SIZE * self.size),
                                bd=3, relief='solid')
        self.canvas.pack(side="left")
        self.canvas2 = tk.Canvas(self.window, width=(TILE_SIZE * self.size),
                                 height=(TILE_SIZE * self.size),
                                 bd=3, relief='solid')
        self.canvas2.pack(side="left")
        self.window.bind("<Key>", self._key_input)
        self._reset()

    def _reset(self):
        self.game = SnakeGameLoop(self.size)
        self.board_memory = self.game.get_board()
        self.board_memory2 = self.game.get_board()
        self._draw_board()
        self.window.after(TICK_TIME, self._tick)
        self.game_over = False
        self._set_board()

    @timeit
    def _set_board(self):
        super()._set_board()
        self.board_rectangles2 = []
        board2 = self.game.get_board()
        for i, row in enumerate(board2):
            rectangles_row2 = []
            for j, cell in enumerate(row):
                rectangles_row2.append(self.canvas2.create_rectangle(TILE_SIZE * j, TILE_SIZE * i,
                                                                     TILE_SIZE * (j + 1), TILE_SIZE * (i + 1),
                                                                     fill=SYMBOLS_COLORS[cell]))
            self.board_rectangles2.append(rectangles_row2)

    @timeit
    def _draw_board(self):
        super()._set_board()
        board2 = self.game.get_board()
        for i, row in enumerate(board2):
            for j, cell in enumerate(row):
                if self.board_memory2[i][j] != cell:
                    self.canvas2.itemconfig(self.board_rectangles2[i][j], fill=SYMBOLS_COLORS[cell])
        self.board_memory2 = board2
