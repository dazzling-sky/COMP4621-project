import socket
import sys

def handle_request(conn_from_proxy, conn_from_browser):
    if conn_from_proxy is not None:
                
        response_header = "HTTP/1.1 200 Connection established\r\nProxy-agent: python proxy\n\n"
        conn_from_browser.send(response_header.encode())
                    
        conn_from_proxy.setblocking(0)
        conn_from_browser.setblocking(0)
       
        isLastRequest, isLastResponse = False, False

        while True:
            if isLastRequest == True and isLastResponse == True:
                break
            try:
                request = conn_from_browser.recv(4096)
                
                if request.strip():
                    isLastRequest = False
                    conn_from_browser.setblocking(0)
                else:
                    isLastRequest = True
                    conn_from_browser.settimeout(20)
                    
                conn_from_proxy.send(request)

            except socket.error:
                pass

            try:
                response = conn_from_proxy.recv(4096)
                if response.strip():
                    isLastResponse = False
                    conn_from_proxy.setblocking(0)
                else:
                    isLastResponse = True              
                    conn_from_proxy.settimeout(20)
                    
                conn_from_browser.send(response)

            except socket.error:
                pass

        sys.exit(0)