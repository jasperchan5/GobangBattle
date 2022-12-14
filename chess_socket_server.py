import socket
import socket
import time
import random
from _thread import *

color = {"RED": 0, "ORANGE": 1, "YELLOW": 2,
         "GREEN": 3, "BLUE": 4, "PURPLE": 5}


class Server:
    def __init__(self, HOST, PORT):
        HOST, PORT = "127.0.0.1", (5039 + 1023) % 65535
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((HOST, PORT))

    def sendColor(color, playerNum):
        for i in range(playerNum):

    def sendRequest():
        msg = 'gogogo'
        clientSocket.send(msg)

    # def getPosition():


class Client:
    def __init__(self, HOST, PORT):
        # server IP, Port
        self.HOST = HOST
        self.PORT = PORT
        # connect to server
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((HOST, PORT))

    def getColor():

    def getRequest():
        response = clientSocket.recv(4096)
        response.decode()
    # def sendPosition():



#while !FINISH do
#for i in allplayers AND !FINISH do
#    newStep < - RETURN player[i].sendRequest()

#    if WIN(newStep, i) then
#        player[i].WIN < - TRUE AND FINISH < - TRUE

#        for j in allplayers AND j /= i do
#        UPDATE(newStep)


#for i in allplayers do
#player[i].sendFinish()





