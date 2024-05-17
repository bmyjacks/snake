import time

import numpy as np

from config import Config


class SnakeLogic:
    def __init__(self, ui):
        self.ui = ui
        self.config = Config()

        self.speed = self.config.getint('Game', 'Speed')

        self.start_time = time.time()
        self.dx, self.dy = 1 * self.speed, 0 * self.speed  # Initial direction of the snake
        self.board_size = Config().getint('Game', 'BoardSize')
        self.snake = np.vstack([[self.board_size // 2, self.board_size // 2],
                                [self.board_size // 2 - 1, self.board_size // 2 - 1]], dtype=int)

        self.move_snake()

    def get_duration(self):
        return time.time() - self.start_time

    def get_snake(self):
        return self.snake

    def move_snake(self):
        head = self.snake[0]
        new_head = head + [self.dx, self.dy]
        if new_head[0] < 0 or new_head[0] >= self.board_size:
            new_head[0] = self.board_size - new_head[0]

        self.snake = np.vstack([new_head, self.snake[:-1]])
        self.ui.after(1000 // self.speed, self.move_snake)

    def change_direction(self, new_dx, new_dy):
        self.dx, self.dy = new_dx, new_dy

    def move_up(self):
        self.change_direction(0, -2)

    def move_down(self):
        self.change_direction(0, 2)

    def move_left(self):
        self.change_direction(-2, 0)

    def move_right(self):
        self.change_direction(2, 0)
