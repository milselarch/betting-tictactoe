import game
import board
import multiplayer

from threading import Thread

# https://docs.python.org/3/library/threading.html
# https://benedictwilkinsai.github.io/post/tkinter-mp/

# create GUI window
gui_board = board.init_board(start=False)
# attach write event hook to wrapper board object
game.on_board_update = gui_board.set_board
game.on_board_reset = gui_board.reset_board
multiplayer.on_board_update = gui_board.set_board
multiplayer.on_board_reset = gui_board.reset_board
game_func = None

while game_func is None: 
    use_multiplayer = input('multiplayer? (y/n) ')
    use_multiplayer = use_multiplayer.strip()

    if use_multiplayer == 'n':
        game_func = game.game
    elif use_multiplayer == 'y':
        game_func = multiplayer.main
    else:
        print(f'Invalid input: {use_multiplayer}')

# start terminal-based game
thread = Thread(target=game_func)
thread.start()

# run gui main event loop
gui_board.mainloop()
    