import tkinter as tk
from tkinter import ttk

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

        self.right_menu = ttk.Frame(self, width=200)
        self.duration_label = ttk.Label(self.right_menu, text="Duration:")
        self.duration_label.pack()
        self.duration_text = ttk.Label(self.right_menu, text="0.00 seconds")
        self.duration_text.pack()
        self.right_menu.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.board = ttk.Frame(self)
        self.canvas = tk.Canvas(self.board, bg='black')
        self.canvas.pack()
        self.board.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.logic = SnakeLogic(self)

        self.bind('<Configure>', self.update_layout)

        self.update_duration()
        self.update_snake()

    def update_layout(self, event):
        self.canvas.config(width=self.board.winfo_width(), height=self.board.winfo_height())
        self.cell_size_x = self.canvas.winfo_width() // self.board_size
        self.cell_size_y = self.canvas.winfo_height() // self.board_size

    def update_duration(self):
        duration = self.logic.get_duration()
        self.duration_text.config(text=f"{duration:.2f} seconds")
        self.after(500, self.update_duration)

    def get_position(self, cell_x, cell_y):
        x = cell_x * self.cell_size_x
        y = cell_y * self.cell_size_y
        return x, y

    def update_snake(self):
        self.canvas.delete('all')
        snake = self.logic.get_snake()
        for cell in snake:
            cell_x, cell_y = cell
            x, y = self.get_position(cell_x, cell_y)
            self.canvas.create_rectangle(x, y, x + self.cell_size_x, y + self.cell_size_y, fill='white')

        self.after(1000 // self.update_speed, self.update_snake)
