import getpass
import time

from libdw import pyrebase
from time import sleep

def on_board_update(board):
    # callback function for when board is updated
    # meant to be overriden
    pass

def on_board_reset(board):
    # callback function for when board is reset
    # meant to be overriden
    pass

InitCash = 100
RULES = '[rules]'
SLEEP = 3
GOODBYE = 'See you next time!'
CHESS = [" ", "X", "O"]

projectid = "sutd-utational-project"
dburl = "https://" + projectid + ".firebaseio.com"
authdomain = projectid + ".firebaseapp.com"
apikey = "AIzaSyCro0vqZ8o0vPK7CkmgAiefXhbZE47hpNQ"
email = "milselarch@gmail.com"
password = "potatopotato"

condition = ''
running = 0

config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()
user = auth.refresh(user['refreshToken'])

key = "data"


def getData():
    node = db.child(key).get(user['idToken'])
    return dict(node.val())


def setData(value):
    db.child(key).set(value, user['idToken'])

def initialize(game):
    game["playerNum"] = 0
    game["gameIsReady"] = False
    game["player1Name"] = ''
    game["player2Name"] = ''
    game["winner"] = 'None'
    game["stage"] = 'bid'
    
    timestamp = time.time()
    game["timestamp_p1"] = timestamp
    game["timestamp_p2"] = timestamp

    game["player1Cash"] = InitCash
    game["player2Cash"] = InitCash
    game["currentPlayer"] = 1
    game["occupied"] = False  # Show whether a player is entering name
    game["bid1"] = 0  # The bid
    game["bid2"] = 0
    game["info"] = 'None'
    game["turn"] = 0
    game["board"] = [
        CHESS[0], CHESS[0], CHESS[0], CHESS[0],
        CHESS[0], CHESS[0], CHESS[0], CHESS[0], 
        CHESS[0], CHESS[0]
    ]

    on_board_reset({
        str(k): game["board"][k] 
        for k in range(len(game["board"]))
    })
    return


def showStatus(game):
    print(game["player1Name"] + " you have " + str(game["player1Cash"]))
    print(game["player2Name"] + " you have " + str(game["player2Cash"]))


def showBoard(game):
    on_board_update({
        str(k): game["board"][k] 
        for k in range(len(game["board"]))
    })

    print(game["board"][7] + '|' + game["board"][8] + '|' + game["board"][9])
    print('-+-+-')
    print(game["board"][4] + '|' + game["board"][5] + '|' + game["board"][6])
    print('-+-+-')
    print(game["board"][1] + '|' + game["board"][2] + '|' + game["board"][3])


def newGame(game):
    game["occupied"] = True
    game["playerNum"] += 1
    setData(game)

    if game["gameIsReady"]:
        print("Sorry, the game is already running!")
        return

    if game["playerNum"] == 1:
        game["player1Name"] = input("Please enter your name player 01:")
    if game["playerNum"] == 2:
        game["player2Name"] = input("Please enter your name player 02:")
        game["gameIsReady"] = True

    game["occupied"] = False
    setData(game)
    return game["playerNum"]


def getWinner(game):
    # return piece (X or O) of winning player
    # returns None if there's no winner

    if game["board"][7] == game["board"][8] == game["board"][9] != ' ':  # across the top
        return game["board"][7]

    elif game["board"][4] == game["board"][5] == game["board"][6] != ' ':  # across the middle
        return game["board"][4]

    elif game["board"][1] == game["board"][2] == game["board"][3] != ' ':  # across the bottom
        return game["board"][1]

    elif game["board"][1] == game["board"][4] == game["board"][7] != ' ':  # down the left side
        return game["board"][1]

    elif game["board"][2] == game["board"][5] == game["board"][8] != ' ':  # down the middle
        return game["board"][2]

    elif game["board"][3] == game["board"][6] == game["board"][9] != ' ':  # down the right side
        return game["board"][3]

    elif game["board"][7] == game["board"][5] == game["board"][3] != ' ':  # diagonal
        return game["board"][7]

    elif game["board"][1] == game["board"][5] == game["board"][9] != ' ':  # diagonal
        return game["board"][1]

    return 'None'


def getBid(playerID, game):
    while True:
        if game["info"] == "SameBid":
            print("Same bid, bid again!")
        try:
            bid = input("player bid:")
            bid = int(bid)
        except:
            print("Invalid input, try again!")
        if bid > game["player"+str(playerID)+"Cash"]:
            print('You bid more than you own! Try again')
        elif bid < 0:
            print("dude you can't bid a negative amount. Try again")
        else:
            game["bid"+str(playerID)] = bid
            break

    if playerID == 1:
        game["currentPlayer"] = 2

    if playerID == 2:
        if game["bid1"] == game["bid2"]:
            game["info"] = "SameBid"
            game["bid1"] = 0
            game["bid2"] = 0
            game["currentPlayer"] = 1
        else:
            game["info"] = 'None'
            if game["bid1"] > game["bid2"]:
                game["currentPlayer"] = 1
                game["stage"] = "move"
                game["player1Cash"] -= game["bid1"]
                game["player2Cash"] += game["bid1"]
                game["bid1"] = 0
                game["bid2"] = 0
                game["info"] = "Player 1 won the bid!"
            if game["bid1"] < game["bid2"]:
                game["currentPlayer"] = 2
                game["stage"] = "move"
                game["player1Cash"] += game["bid2"]
                game["player2Cash"] -= game["bid2"]
                game["bid1"] = 0
                game["bid2"] = 0
                game["info"] = "Player 2 won the bid!"

    setData(game)
    return

def getMove(playerID, game):
    while True:
        try:
            move = int(input(
                "Please enter a number from 1-9 representing your play:"
            ))
        except ValueError:
            print('Invalid input, try again')
            continue

        if game["board"][move] != CHESS[0]:
            print('That space has been taken up already, please enter another number')
        else:
            game["board"][move] = CHESS[playerID]

            on_board_update({
                str(k): game["board"][k] 
                for k in range(len(game["board"]))
            })
            break
        
    game["info"] = 'None'
    game["turn"] += 1
    game["winner"] = getWinner(game)

    if game["turn"] == 9 and game["winner"] == 'None':
        game["winner"] = "Draw"
        return

    game["stage"] = "bid"
    game["currentPlayer"] = 1
    setData(game)
    return

def endGame(game):
    initialize(game)


def main():
    game = {}
    playerID = 0
    initialize(game)
    
    # Introduction
    print(
        "Hello! Welcome to Bidding Tic-Tac-Toe. \n" +
        RULES + "\n Both players start with $100"
    )
    print(
        "Player 1 is " + CHESS[1] + 
        " and Player 2 is " + CHESS[2] +
        ". The board is arranged like a number pad with your play being a number from 1-9"
    )
    
    running = 1
    condition = input("Start Game (Y/N):")
    game = getData()

    if game["gameIsReady"]:
        while True:
            # wait until someone isn't playing
            # as one of the players
            game = getData()
            timestamp = time.time()
            duration1 = timestamp - game['timestamp_p1']
            duration2 = timestamp - game['timestamp_p2']
            
            if (duration1 > 60) or (duration2 > 60):
                break

            print('People are already playing. wait a bit')
            sleep(3)

        if duration1 > 60:
            playerID = 1
        elif duration2 > 60:
            # if second player hasn't played in 1 munute
            # you become second player
            playerID = 2

    while running:
        sleep(SLEEP)
        
        try:
            game = getData()
        except:
            print("loading...")

        if condition == 'Y':
            if not game["gameIsReady"] and playerID == 0:
                if game["occupied"] == True:
                    print("Wait for another player to enter name!")
                else:
                    playerID = newGame(game)

            if not game["gameIsReady"] and playerID != 0:
                print("Wait for another player to enter name!")

            if game["gameIsReady"]:
                if playerID == 1:
                    game["timestamp_p1"] = time.time()
                else:
                    game["timestamp_p2"] = time.time()

                setData(game)
                
                if game["winner"] != 'None':
                    if game["winner"] == CHESS[playerID]:
                        print("Congratulation! You won!")
                    elif game["winner"] == "Draw":
                        print("It's a draw.")
                    else:
                        print(game[
                            "player" + str(3-playerID) + "Name"
                            ] +" won."
                        )
                    
                    condition = 'N'
                    continue
                
                if game["currentPlayer"] != playerID:
                    print("It's not your turn now!")
                    showStatus(game)
                    showBoard(game)

                    if game["stage"] == "move":
                        print(game["info"])

                    continue

                if game["currentPlayer"] == playerID:
                    showStatus(game)
                    showBoard(game)

                    if game["stage"] == "bid":
                        getBid(playerID, game)
                    if game["stage"] == "move":
                        getMove(playerID, game)

            continue

        if condition == 'N':
            running = 0
            endGame(game)
            setData(game)
            print(GOODBYE)
            sleep(3)
            continue

        condition = input("Start Game(Y/N):")


if __name__ == '__main__':
    main()
