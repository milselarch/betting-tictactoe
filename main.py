import game
import board

from threading import Thread

# https://docs.python.org/3/library/threading.html
# https://benedictwilkinsai.github.io/post/tkinter-mp/

# create GUI window
gui_board = board.init_board(start=False)
# wrap game board with board.Board
game.board = board.Board(game.board)
# attach write event hook to wrapper board object
game.board.attach_trigger(gui_board.set_board)

# start terminal-based game
thread = Thread(target=game.game)
thread.start()

# run gui main event loop
gui_board.mainloop()
    