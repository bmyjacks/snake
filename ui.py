import tkinter as tk

from config import Config
from logic import SnakeLogic


class Snake(tk.Tk):
    """
    The Snake class is a subclass of tkinter's Tk class and represents the main application window.
    It handles the UI and game logic for the snake game.
    """

    def __init__(self):
        """
        Initialize the Snake game. Set up the game board, score, duration, and controls.
        """
        super().__init__()
        self._config = Config()
        self._board_size = self._config.getint('Game', 'BoardSize')
        self._cell_size_x = self._board_size
        self._cell_size_y = self._board_size
        self._update_speed = self._config.getint('Game', 'Speed')

        self.title(self._config.get('UI', 'Title'))
        self.geometry(self._config.get('UI', 'Size'))
        self.resizable(self._config.getboolean('UI', 'Resizable'), self._config.getboolean('UI', 'Resizable'))

        # Set up the right menu with duration and score labels, and a quit button
        self._right_menu = tk.Frame(self, width=100)
        self._duration_label = tk.Label(self._right_menu, text="Duration:")
        self._duration_label.pack()
        self._duration_text = tk.Label(self._right_menu, text="0.00 seconds")
        self._duration_text.pack()
        self._score_label = tk.Label(self._right_menu, text="Score:")
        self._score_label.pack()
        self._score_text = tk.Label(self._right_menu, text="0")
        self._score_text.pack()
        self._quit_button = tk.Button(self._right_menu, text="Quit", command=self.quit)
        self._quit_button.pack()
        self._right_menu.pack(side=tk.RIGHT, fill=tk.Y, expand=True, padx=10, pady=10)

        # Set up the game board with a black background
        self._board = tk.Frame(self, bg='black')
        self._canvas = tk.Canvas(self._board, bg='black')
        self._canvas.pack()
        self._board.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self._logic = SnakeLogic(self)

        # Bind keyboard events to game controls
        self.bind('<Configure>', self.update_layout)
        self.bind('<Up>', lambda e: self._logic.move_up())
        self.bind('<Down>', lambda e: self._logic.move_down())
        self.bind('<Left>', lambda e: self._logic.move_left())
        self.bind('<Right>', lambda e: self._logic.move_right())

        # Start the game
        self.update_duration()
        self.update_score()
        self.draw_snake()
        self.draw_food()

    def update_layout(self, event):
        """
        Update the layout of the game board when the window is resized.
        """
        self._canvas.config(width=self._board.winfo_width(), height=self._board.winfo_height())
        self._cell_size_x = self._canvas.winfo_width() // self._board_size
        self._cell_size_y = self._canvas.winfo_height() // self._board_size

    def update_duration(self):
        """
        Update the duration label with the current game duration.
        """
        duration = self._logic.get_duration()
        self._duration_text.config(text=f"{duration:.2f} seconds")
        if not self._logic.get_finished():
            self.after(1000 // self._update_speed, self.update_duration)

    def update_score(self):
        """
        Update the score label with the current game score.
        """
        score = self._logic.get_score()
        self._score_text.config(text=score)

        if not self._logic.get_finished():
            self.after(1000 // self._update_speed, self.update_score)

    def get_position(self, cell_x, cell_y):
        """
        Convert cell coordinates to pixel coordinates.
        """
        x = cell_x * self._cell_size_x
        y = cell_y * self._cell_size_y
        return x, y

    def draw_food(self):
        """
        Draw the food on the game board.
        """
        self._canvas.delete('food')
        food = self._logic.get_food()
        for cell in food:
            cell_x, cell_y = cell
            x, y = self.get_position(cell_x, cell_y)
            self._canvas.create_rectangle(x, y, x + self._cell_size_x, y + self._cell_size_y, fill='green', tags='food')

        if not self._logic.get_finished():
            self.after(1000 // self._update_speed, self.draw_food)

    def draw_snake(self):
        """
        Draw the snake on the game board. If the game is over, display a game over message.
        """
        self._canvas.delete('snake')
        snake = self._logic.get_snake()
        for cell in snake:
            cell_x, cell_y = cell
            x, y = self.get_position(cell_x, cell_y)
            self._canvas.create_rectangle(x, y, x + self._cell_size_x, y + self._cell_size_y, fill='red', tags='snake')

        if self._logic.get_finished():
            self._canvas.create_text(self._canvas.winfo_width() // 2, self._canvas.winfo_height() // 2,
                                     text="Game Over",
                                     fill='white', font=('Arial', 40))
        else:
            self.after(1000 // self._update_speed, self.draw_snake)
