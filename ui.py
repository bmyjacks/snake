import tkinter as tk

from config import Config
from logic import SnakeLogic


class Snake(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.board_size = self.config.getint('Game', 'BoardSize')
        self.cell_size_x = self.board_size
        self.cell_size_y = self.board_size
        self.update_speed = self.config.getint('Game', 'Speed')

        self.title(self.config.get('UI', 'Title'))
        self.geometry(self.config.get('UI', 'Size'))
        self.resizable(self.config.getboolean('UI', 'Resizable'), self.config.getboolean('UI', 'Resizable'))

        self.right_menu = tk.Frame(self, width=100)
        self.duration_label = tk.Label(self.right_menu, text="Duration:")
        self.duration_label.pack()
        self.duration_text = tk.Label(self.right_menu, text="0.00 seconds")
        self.duration_text.pack()
        self.score_label = tk.Label(self.right_menu, text="Score:")
        self.score_label.pack()
        self.score_text = tk.Label(self.right_menu, text="0")
        self.score_text.pack()
        self.quit_button = tk.Button(self.right_menu, text="Quit", command=self.quit)
        self.quit_button.pack()
        self.right_menu.pack(side=tk.RIGHT, fill=tk.Y, expand=True, padx=10, pady=10)

        self.board = tk.Frame(self, bg='black')
        self.canvas = tk.Canvas(self.board, bg='black')
        self.canvas.pack()
        self.board.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.logic = SnakeLogic(self)

        self.bind('<Configure>', self.update_layout)
        self.bind('<Up>', lambda e: self.logic.move_up())
        self.bind('<Down>', lambda e: self.logic.move_down())
        self.bind('<Left>', lambda e: self.logic.move_left())
        self.bind('<Right>', lambda e: self.logic.move_right())

        self.update_duration()
        self.update_score()
        self.draw_snake()
        self.draw_food()

    def update_layout(self, event):
        self.canvas.config(width=self.board.winfo_width(), height=self.board.winfo_height())
        self.cell_size_x = self.canvas.winfo_width() // self.board_size
        self.cell_size_y = self.canvas.winfo_height() // self.board_size

    def update_duration(self):
        duration = self.logic.get_duration()
        self.duration_text.config(text=f"{duration:.2f} seconds")
        if not self.logic.get_finished():
            self.after(1000 // self.update_speed, self.update_duration)

    def update_score(self):
        score = self.logic.get_score()
        self.score_text.config(text=score)

        if not self.logic.get_finished():
            self.after(1000 // self.update_speed, self.update_score)

    def get_position(self, cell_x, cell_y):
        x = cell_x * self.cell_size_x
        y = cell_y * self.cell_size_y
        return x, y

    def draw_food(self):
        self.canvas.delete('food')
        food = self.logic.get_food()
        for cell in food:
            cell_x, cell_y = cell
            x, y = self.get_position(cell_x, cell_y)
            self.canvas.create_rectangle(x, y, x + self.cell_size_x, y + self.cell_size_y, fill='green', tags='food')

        if not self.logic.get_finished():
            self.after(1000 // self.update_speed, self.draw_food)

    def draw_snake(self):
        self.canvas.delete('snake')
        snake = self.logic.get_snake()
        for cell in snake:
            cell_x, cell_y = cell
            x, y = self.get_position(cell_x, cell_y)
            self.canvas.create_rectangle(x, y, x + self.cell_size_x, y + self.cell_size_y, fill='red', tags='snake')

        if self.logic.get_finished():
            self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, text="Game Over",
                                    fill='white', font=('Arial', 40))
        else:
            self.after(1000 // self.update_speed, self.draw_snake)
