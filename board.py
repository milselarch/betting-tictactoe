# https://effbot.org/tkinterbook/canvas.htm
# https://stackoverflow.com/questions/51944799/python-tkinter-textvariable-in-label-widget/51945554

import tkinter as tk
import copy


class Board(object):
    def __init__(self, init_board):
        self.init_board = copy.deepcopy(init_board)
        self.trigger = lambda *x: None
        self.board = init_board

    def attach_trigger(self, trigger):
        self.trigger = trigger

    def __setitem__(self, key, item):
        self.board[key] = item
        self.trigger(self.board)
    
    def __getitem__(self, key):
        return self.board[key]


class BoardGui(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("Tic Tac Toe Board")
        self.state = {}
        self.labels = {}
        self.make()

        self.master.config(bg='grey92')
        self['bg'] = 'grey92'
        self.master.grid_columnconfigure(100, weight=1)
        self.master.grid_rowconfigure(100, weight=1)
        self.grid(
            row=100, column=100,
            padx=5, pady=5
        )

    def reset_board(self):
        for k in range(3):
            for i in range(3):
                string_var = self.state[(k, i)]
                string_var.set(f'{3 * k + i + 1}')

    def set_board(self, board):
        for key in board:
            str_key = str(key)

            if board[str_key] == ' ':
                continue

            index = int(key)
            k = (index - 1) // 3
            i = (index - 1) % 3

            string_var = self.state[(k, i)]
            string_var.set(board[str_key])

    def make(self):
        self.left_buffer = tk.Frame(self, width=10, height=10)
        self.left_buffer.grid(row=100, column=000, sticky="nsew")
        self.right_buffer = tk.Frame(self, width=10, height=10)
        self.right_buffer.grid(row=100, column=200, sticky="nsew")
        self.top_buffer = tk.Frame(self, width=10, height=10)
        self.top_buffer.grid(row=000, column=100, sticky="nsew")
        self.bottom_buffer = tk.Frame(self, width=10, height=10)
        self.bottom_buffer.grid(row=200, column=100, sticky="nsew")

        self.holder = tk.Frame(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(200, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(200, weight=1)
        self.holder.grid(row=100, column=100)
        
        for k in range(3):
            for i in range(3):
                string_var = tk.StringVar()

                label = tk.Label(
                    self.holder, textvariable=string_var,
                    width=2, height=2,
                    font=("Courier New", 44, 'bold'), bg='white'
                )

                label.grid(
                    row=(3 - k) * 100, column=i * 100,
                    padx=5, pady=5, ipadx=20
                )
                
                self.state[(k, i)] = string_var
                self.labels[(k, i)] = label

        self.reset_board()


def init_board(start=True):
    root = tk.Tk()
    root = BoardGui(root)

    if start:
        root.mainloop()

    return root

if __name__ == '__main__':
    init_board()

    

    