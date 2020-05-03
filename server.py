import socket
import threading
import threads

serverPort = 12000

# website to test http: http://www.apache.org
# website to test https: https://www.google.com

proxySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

proxySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxySocket.bind(('',serverPort))
proxySocket.listen(1)


print('The server is ready to receive...' + '\n')

while (1):
    conn_from_browser, incoming_addr = proxySocket.accept()

    #create new thread for incoming request
    proxy_thread = threads.ProxyThread(conn_from_browser)
    
    #Start new thread
    proxy_thread.start()

    #Add thread to the list and increment count

conn_from_browser.close()



