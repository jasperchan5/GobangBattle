import socket
from _thread import *
import time
import random

ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
nowPlayer = -1
Finish = False
Winner = -1

board_size = 15
board = []
for i in range(board_size):
    board.append([])
    for j in range(board_size):
      board[i].append(0)
newPositionX = -1
newPositionY = -1
newcolor = ""

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(4)


def send_color(connection, color):
    connection.send(str.encode(color))

def gamestart(connection, color, id):
    #global nowPlayer
    global newPositionX
    global newPositionY

    print(connection)
    
    send_color(connection, color)

    while nowPlayer == -1:
        continue

    while not Finish:
        if id == nowPlayer:
            # ask player to play
            # newposition = get the position the player played
            connection.send(str.encode("your_turn"))
            try:
                newPosition = connection.recv(1024).decode("utf-8")
                # print(newPosition)
                # print(newPosition[0])
                # print(newPosition[1])
                newPositionX = int(newPosition[0])
                newPositionY = int(newPosition[1])
                newcolor = color
            except:
                continue
            
        else:
            connection.send(str.encode("not_your_turn"))
            while newPositionX == -1 and newPositionY == -1:
                continue
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
random.shuffle(color_list)
Client_list = []
while ThreadCount < 4:
    Client, address = ServerSideSocket.accept()
    Client_list.append(Client)
    start_new_thread(gamestart, (Client_list[ThreadCount], color_list[ThreadCount], ThreadCount))
    ThreadCount += 1

nowPlayer = 0
time.sleep(3)

while not Finish:
    while newPositionX == -1 and newPositionY == -1:
        continue
    while board[newPositionX][newPositionY]:
        continue
    time.sleep(3)
    board[newPositionX][newPositionY] = True
    if Finish:
        Winner = nowPlayer # check if the current player win: set Winner to nowPlayer
        break
    nowPlayer = (nowPlayer + 1) % 4
    print("nowPlayer=", nowPlayer, "\n")
    
print("out")    

ServerSideSocket.close()
