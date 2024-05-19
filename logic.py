import time

import numpy as np

from config import Config


class SnakeLogic:
    def __init__(self, ui):
        self.ui = ui
        self.config = Config()

        self.speed = self.config.getint('Game', 'Speed')
        self.finished = False
        self.rng = np.random.default_rng(self.config.getint('Game', 'FoodGenerateSeed'))

        self.start_time = time.time()
        self.dx, self.dy = 1, 0  # Initial direction and speed of each axis
        self.board_size = Config().getint('Game', 'BoardSize')
        self.snake = np.vstack([[self.board_size // 2, self.board_size // 2],
                                [self.board_size // 2 - 1, self.board_size // 2],
                                [self.board_size // 2 - 2, self.board_size // 2]], dtype=int)
        self.food = list()

        self.new_food()
        self.move_snake()

    def get_duration(self):
        return time.time() - self.start_time

    def get_snake(self):
        return self.snake

    def get_score(self):
        return len(self.snake) - 3

    def is_snake(self, x, y):
        return (self.snake == [x, y]).all(axis=1).any()

    def judge(self):
        head = self.snake[0]
        body = self.snake[1:]
        if head[0] < 0 or head[0] >= self.board_size or head[1] < 0 or head[1] >= self.board_size:
            self.finished = True
        if (head == body).all(axis=1).any():
            self.finished = True

    def get_finished(self):
        return self.finished

    def longer_snake(self):
        last_1 = self.snake[-1]
        last_2 = self.snake[-2]

        new_cell = last_1 + (last_1 - last_2)
        self.snake = np.vstack([self.snake, new_cell])

    def move_snake(self):
        head = self.snake[0]
        new_head = head + [self.dx, self.dy]

        if (new_head == self.food[0]).all():
            self.new_food()
            self.longer_snake()

        self.snake = np.vstack([new_head, self.snake[:-1]])
        self.judge()

        if not self.finished:
            self.ui.after(1000 // self.speed, self.move_snake)

    def get_food(self):
        return self.food

    def new_food(self):
        self.food = self.food[1:]
        new_food = [self.rng.integers(0, self.board_size), self.rng.integers(0, self.board_size)]
        while self.is_snake(*new_food):
            new_food = [self.rng.integers(0, self.board_size), self.rng.integers(0, self.board_size)]
        self.food.append(new_food)

    def change_direction(self, new_dx, new_dy):
        self.dx, self.dy = new_dx, new_dy

    def move_up(self):
        self.change_direction(0, -1)

    def move_down(self):
        self.change_direction(0, 1)

    def move_left(self):
        self.change_direction(-1, 0)

    def move_right(self):
        self.change_direction(1, 0)
