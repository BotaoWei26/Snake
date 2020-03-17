from snake_graphics import SnakeGraphics, SYMBOLS_COLORS, DIRECTION_KEYS
import tkinter as tk
from snake_game_loop import SnakeGameLoop
from math import ceil
import socket

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

        self._set_connection()

        self.window.bind("<Key>", self._key_input)
        self._reset()

    def _set_connection(self):
        self.c = socket.socket()
        self.c.connect((input("Server Address: "), 9999))
        self.c.recv(256)

    def _reset(self):
        self.game = SnakeGameLoop(self.size)
        self.board_memory = self.game.get_board()
        self.board_memory2 = self.game.get_board()
        self.game_over = False
        self._set_board()
        self._draw_board()
        self.window.after(TICK_TIME, self._tick)

    def _tick(self):
        self.game.move_snake()
        self._draw_board()
        if not self._check_gameover():
            self.window.after(TICK_TIME, self._tick)
        else:
            self.game_over = True
            self.c.send(bytes("over","utf-8"))

    def _key_input(self, event):
        if self.game_over:
            self.c.recv(256)
            self._reset()
        elif event.char in DIRECTION_KEYS.values():
            self.game.change_direction(event.char)

    def _set_board(self):
        super()._set_board()
        self.board_rectangles2 = []
        self._send_board(self.game.get_board())
        board2 = self._get_other_board()
        for i, row in enumerate(board2):
            rectangles_row2 = []
            for j, cell in enumerate(row):
                rectangles_row2.append(self.canvas2.create_rectangle(TILE_SIZE * j, TILE_SIZE * i,
                                                                     TILE_SIZE * (j + 1), TILE_SIZE * (i + 1),
                                                                     fill=SYMBOLS_COLORS[cell]))
            self.board_rectangles2.append(rectangles_row2)

    def _draw_board(self):
        super()._draw_board()
        self._send_board(self.board_memory)
        board2 = self._get_other_board()
        if board2 == "over":
            return
        for i, row in enumerate(board2):
            for j, cell in enumerate(row):
                if self.board_memory2[i][j] != cell:
                    self.canvas2.itemconfig(self.board_rectangles2[i][j], fill=SYMBOLS_COLORS[cell])
        self.board_memory2 = board2

    def _get_other_board(self):
        other_info = self.c.recv(1024).decode()
        if other_info == "over":
            self.game_over = True
            return
        return self._decode_board(other_info)

    def _send_board(self, board):
        self.c.send(self._encode_board(board))

    def _decode_board(self, info):
        board = []
        count = 0
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(info[count])
                count += 1
            board.append(row)
        return board

    def _encode_board(self, board):
        info = ""
        for row in board:
            for cell in row:
                info += cell
        return bytes(info,"utf-8")
