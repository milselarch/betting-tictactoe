# https://effbot.org/tkinterbook/canvas.htm
# https://stackoverflow.com/questions/51944799/python-tkinter-textvariable-in-label-widget/51945554

import tkinter as tk
import copy
import get_input

input = get_input.get_input

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

    def reset_board(self, *args):
        """
        Reset the GUI board such that is displays only
        the numerical positions of each tile, and sets
        the color of each tile to a light grey
        """
        for k in range(3):
            for i in range(3):
                string_var = self.state[(k, i)]
                label = self.labels[(k, i)]
                string_var.set(f'{3 * k + i + 1}')
                label.config(fg='grey52')

    def set_board(self, board):
        """
        given a dictionary representing the state of the tictactoe
        board, update the corresponding tiles in the GUI. 

        The board dictionary should contains string keys 
        '1', '2', ..., '9', and values corresponding to either
        'O', 'X', or ' '
        """

        for key in board:
            str_key = str(key)
            assert board[str_key] in ('O', 'X', ' ')

            if board[str_key] == ' ':
                continue

            index = int(key)
            k = (index - 1) // 3
            i = (index - 1) % 3

            string_var = self.state[(k, i)]
            player_move = board[str_key]
            string_var.set(player_move)
            label = self.labels[(k, i)]

            if player_move == 'X':
                label.config(fg='red')
            else:
                label.config(fg='blue')

    def make(self):
        """
        buffers here are expandable widgets
        used to make the main tictactoe board center
        regardless of how the window is stretched or shrunk
        """
        self.left_buffer = tk.Frame(self, width=10, height=10)
        self.left_buffer.grid(row=100, column=000, sticky="nsew")
        self.right_buffer = tk.Frame(self, width=10, height=10)
        self.right_buffer.grid(row=100, column=200, sticky="nsew")
        self.top_buffer = tk.Frame(self, width=10, height=10)
        self.top_buffer.grid(row=000, column=100, sticky="nsew")
        self.bottom_buffer = tk.Frame(self, width=10, height=10)
        self.bottom_buffer.grid(row=200, column=100, sticky="nsew")

        self.holder = tk.Frame(self)
        # make rows 0, 200, columns 0, 200 expandable
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(200, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(200, weight=1)
        self.holder.grid(row=100, column=100)
        
        # initialize labels representing tiles in board
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

    

    