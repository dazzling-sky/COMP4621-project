from socket import *

serverName = gethostbyname(gethostname())
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input('Input lowercase sentence:')
arr = bytes(sentence, 'utf-8')
clientSocket.send(arr)
modifiedSentence = clientSocket.recv(1024)
print('From Server: ', modifiedSentence.decode('utf-8'))
clientSocket.close()


