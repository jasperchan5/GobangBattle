import socket

ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004
print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))
    
color = ""
color = ClientMultiSocket.recv(1024).decode("utf-8")
print(color)

newPositionX = 0
newPositionY = 0
newColor = ""

getPosition = False

while True:
    try:
        message = ClientMultiSocket.recv(1024).decode("utf-8")
        if message == "your_turn":
            print(message)
            while not getPosition:
                continue
            ClientMultiSocket.send(str.encode([str(newPositionX), str(newPositionY)])) # we need to get newposition from JC

        elif message == "not_your_turn":
            print(message)
            step = ClientMultiSocket.recv(1024).decode("utf-8")
            newPositionX = step[0]
            newPositionY = step[1]
            newColor = step[2]
            
        elif message == "you_win":
            # render win in this line
            print(message)
            break

        elif message == "you_lose":
            print(message)
            # render lose in this line
            break
    except:
        continue

ClientMultiSocket.close()