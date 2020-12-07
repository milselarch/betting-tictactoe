import game
import board

from threading import Thread

# https://docs.python.org/3/library/threading.html
# https://benedictwilkinsai.github.io/post/tkinter-mp/

# create GUI window
gui_board = board.init_board(start=False)
# attach write event hook to wrapper board object
game.on_board_update = gui_board.set_board
game.on_board_reset = gui_board.reset_board

# start terminal-based game
thread = Thread(target=game.game)
thread.start()

# run gui main event loop
gui_board.mainloop()
    