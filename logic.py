import time

import numpy as np

from config import Config


class SnakeLogic:
    def __init__(self, ui):
        self._ui = ui
        self._config = Config()

        self._speed = self._config.getint('Game', 'Speed')
        self._finished = False
        self._rng = np.random.default_rng(self._config.getint('Game', 'FoodGenerateSeed'))

        self._start_time = time.time()
        self._dx, self._dy = 1, 0  # Initial direction and speed of each axis
        self._board_size = Config().getint('Game', 'BoardSize')
        self._snake = np.vstack([[self._board_size // 2, self._board_size // 2],
                                 [self._board_size // 2 - 1, self._board_size // 2],
                                 [self._board_size // 2 - 2, self._board_size // 2]], dtype=int)
        self._food = list()

        self.new_food()
        self.move_snake()

    def get_duration(self):
        return time.time() - self._start_time

    def get_snake(self):
        return self._snake

    def get_score(self):
        return len(self._snake) - 3

    def is_snake(self, x, y):
        return (self._snake == [x, y]).all(axis=1).any()

    def judge(self):
        head = self._snake[0]
        body = self._snake[1:]
        if head[0] < 0 or head[0] >= self._board_size or head[1] < 0 or head[1] >= self._board_size:
            self._finished = True
        if (head == body).all(axis=1).any():
            self._finished = True

    def get_finished(self):
        return self._finished

    def longer_snake(self):
        last_1 = self._snake[-1]
        last_2 = self._snake[-2]

        new_cell = last_1 + (last_1 - last_2)
        self._snake = np.vstack([self._snake, new_cell])

    def move_snake(self):
        head = self._snake[0]
        new_head = head + [self._dx, self._dy]

        if (new_head == self._food[0]).all():
            self.new_food()
            self.longer_snake()

        self._snake = np.vstack([new_head, self._snake[:-1]])
        self.judge()

        if not self._finished:
            self._ui.after(1000 // self._speed, self.move_snake)

    def get_food(self):
        return self._food

    def new_food(self):
        self._food = self._food[1:]
        new_food = [self._rng.integers(0, self._board_size), self._rng.integers(0, self._board_size)]
        while self.is_snake(*new_food):
            new_food = [self._rng.integers(0, self._board_size), self._rng.integers(0, self._board_size)]
        self._food.append(new_food)

    def change_direction(self, new_dx, new_dy):
        self._dx, self._dy = new_dx, new_dy

    def move_up(self):
        if self._dy == 0:
            self.change_direction(0, -1)

    def move_down(self):
        if self._dy == 0:
            self.change_direction(0, 1)

    def move_left(self):
        if self._dx == 0:
            self.change_direction(-1, 0)

    def move_right(self):
        if self._dx == 0:
            self.change_direction(1, 0)
