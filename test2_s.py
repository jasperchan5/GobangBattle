import socket
from _thread import *
import time

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 6367
ThreadCount = 0
nowPlayer = 0
Finish = False
Winner = -1

board_size = 15 
board = [[0] * board_size] * board_size

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(4)


def send_color(connection, color):
    connection.send(str.encode(color))

newPositionX = int()
newPositionY = int()
newcolor = ""
def gamestart(connection, color, id):
    # connection.send(str.encode('Server is working:'))
    # print(connection)
    
    send_color(connection, color)

    while not Finish:
        if id == nowPlayer:
            # ask player to play
            # newposition = get the position the player played
            connection.send(str.encode("your_turn"))
            try:
                newPosition = connection.recv(1024).decode("utf-8")
                newPositionX = newPosition[0]
                newPositionY = newPosition[1]
                newcolor = color
            except:
                continue
            
        else:
            connection.send(str.encode("not_your_turn"))
            while board[newPositionX][newPositionY]:
                continue
            connection.send(str.encode([str(newPositionX), str(newPositionY), newcolor]))

    if id == Winner:
        connection.send(str.encode("you_win"))
    else:
        connection.send(str.encode("you_lose"))
    
    time.sleep(10)
    connection.close()


color_list = ["#000000", "#000080", "#008000", "#ff0000", "#800080", "#00ff00", "#00ffff"]
color_list.shuffle()
Client_list = []
while ThreadCount < 5:
    Client, address = ServerSideSocket.accept()
    Client_list.append(Client)
    start_new_thread(gamestart, (Client_list[ThreadCount], color_list[ThreadCount], ThreadCount))
    ThreadCount += 1

time.sleep(3)

while not Finish:
    while board[newPositionX][newPositionY]:
        continue
    time.sleep(3)
    board[newPositionX][newPositionY] = True
    if Finish:
        Winner = nowPlayer # check if the current player win: set Winner to nowPlayer
        break
    nowPlayer = (nowPlayer + 1) % 4
    
ServerSideSocket.close()
