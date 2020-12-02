import game
import board

from threading import Thread

# https://docs.python.org/3/library/threading.html
# https://benedictwilkinsai.github.io/post/tkinter-mp/

print('test')

gui_board = board.init_board(start=False)
game.board = board.Board(game.board)
game.board.attach_trigger(gui_board.set_board)
thread = Thread(target=game.game)
thread.start()

gui_board.mainloop()
    