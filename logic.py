import time

import numpy as np

from config import Config


class SnakeLogic:
    """
    The SnakeLogic class handles the logic of the snake game.
    It is responsible for moving the snake, checking if the game is over, and generating new food.
    """

    def __init__(self, ui):
        """
        Initialize the SnakeLogic class.
        Set up the game board, snake, food, and game speed.
        """
        self._ui = ui
        self._config = Config()

        self._speed = self._config.getint('Game', 'Speed')
        self._finished = False
        self._rng = np.random.default_rng(self._config.getint('Game', 'FoodGenerateSeed'))

        self._start_time = time.time()
        self._dx, self._dy = 1, 0
        self._board_size = Config().getint('Game', 'BoardSize')
        self._snake = np.vstack([[self._board_size // 2, self._board_size // 2],
                                 [self._board_size // 2 - 1, self._board_size // 2],
                                 [self._board_size // 2 - 2, self._board_size // 2]], dtype=int)
        self._food = list()

        self.new_food()
        self.move_snake()

    def get_duration(self):
        """
        Get the duration of the game in seconds.
        """
        return time.time() - self._start_time

    def get_snake(self):
        """
        Get the current position of the snake.
        """
        return self._snake

    def get_score(self):
        """
        Get the current score of the game.
        The score is the length of the snake minus 3.
        """
        return len(self._snake) - 3

    def is_snake(self, x, y):
        """
        Check if the given coordinates are part of the snake.
        """
        return (self._snake == [x, y]).all(axis=1).any()

    def judge(self):
        """
        Check if the game is over.
        The game is over if the snake is out of the board boundaries or if the snake has collided with itself.
        """
        head = self._snake[0]
        body = self._snake[1:]
        if head[0] < 0 or head[0] >= self._board_size or head[1] < 0 or head[1] >= self._board_size:
            self._finished = True
        if (head == body).all(axis=1).any():
            self._finished = True

    def get_finished(self):
        """
        Get the current state of the game.
        If the game is over, return True. Otherwise, return False.
        """
        return self._finished

    def longer_snake(self):
        """
        Make the snake longer by adding a new cell at the end of the snake.
        """
        last_1 = self._snake[-1]
        last_2 = self._snake[-2]

        new_cell = last_1 + (last_1 - last_2)
        self._snake = np.vstack([self._snake, new_cell])

    def move_snake(self):
        """
        Move the snake in the current direction.
        If the snake eats food, generate new food and make the snake longer.
        """
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
        """
        Get the current position of the food.
        """
        return self._food

    def new_food(self):
        """
        Generate new food at a random position on the board that is not part of the snake.
        """
        self._food = self._food[1:]
        new_food = [self._rng.integers(0, self._board_size), self._rng.integers(0, self._board_size)]
        while self.is_snake(*new_food):
            new_food = [self._rng.integers(0, self._board_size), self._rng.integers(0, self._board_size)]
        self._food.append(new_food)

    def change_direction(self, new_dx, new_dy):
        """
        Change the direction of the snake.
        """
        self._dx, self._dy = new_dx, new_dy

    def move_up(self):
        """
        Change the direction of the snake to up.
        """
        if self._dy == 0:
            self.change_direction(0, -1)

    def move_down(self):
        """
        Change the direction of the snake to down.
        """
        if self._dy == 0:
            self.change_direction(0, 1)

    def move_left(self):
        """
        Change the direction of the snake to left.
        """
        if self._dx == 0:
            self.change_direction(-1, 0)

    def move_right(self):
        """
        Change the direction of the snake to right.
        """
        if self._dx == 0:
            self.change_direction(1, 0)
