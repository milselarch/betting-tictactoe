import sys
import time

# https://stackoverflow.com/questions/15817554/obscure-repeatable-crashes-in-multi-threaded-python-console-application-using-t

def get_input(text):
    # input function that hopefully doesn't 
    # junk up tkinter's mainloop
    print(text, end="\n")
    time.sleep(0.1)
    data = sys.stdin.readline()[:-1]
    return data