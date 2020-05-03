import threading
import time
import sys
import socket
import https
import http
import blacklist
import cache

class ProxyThread(threading.Thread):
    def __init__(self, conn_from_browser):
        threading.Thread.__init__(self)
        self.conn_from_browser = conn_from_browser

    def run(self):
        handle_request(self.conn_from_browser)
    

def handle_request(conn_from_browser): 
    request = conn_from_browser.recv(4096)

    # Empty request 
    if not request.strip():
        sys.exit(1)
    
    decoded_request = request.decode('ISO-8859-1')

    server_url = decoded_request.split(' ')[1]

    parsed_url = server_url
    protocol = None 

    # Exclude if http:// or https:// found 
    # Find the protocol (either 'http' or 'https')
    protocol_index = server_url.find('://')
    if protocol_index != -1:
        parsed_url = server_url[protocol_index + 3:]
        protocol = server_url[:protocol_index].lower()
    

    server_host_name = parsed_url.split('/')[0]

    server_port = 80
    if protocol == 'https':
        server_port = 443
    
    # Find the port no attached at the end of url and fix host name
    port_index = parsed_url.find(':')
    resource_index = parsed_url.find('/')

    if port_index != -1:
        if resource_index != -1:
            server_port = parsed_url[port_index + 1:resource_index]
        else:
            server_port = parsed_url[port_index + 1:]

    server_host_name = parsed_url[:port_index]

    resource_index = server_host_name.find('/')

    if resource_index != -1:
        server_host_name = parsed_url[:resource_index]

    if blacklist.in_black_list(server_host_name):
        response_header = 'HTTP/1.1 404 NOT FOUND\n Content-Type: text/html \n\n <HTML> <h1> 404 : Blacklisted on python proxy server </h1> </HTML>'
        conn_from_browser.send(response_header.encode())
        conn_from_browser.close()
        sys.exit(0)

    if cache.cache_exists(server_url):
        data = cache.return_data(server_url)
        conn_from_browser.send(data)
        conn_from_browser.close()
        sys.exit(0)

    
    try:
        conn_from_proxy = socket.create_connection((server_host_name, server_port))

        #Check if request is a CONNECT request
        if decoded_request.split('\n')[0].startswith('CONNECT'):
            https.handle_request(conn_from_proxy, conn_from_browser)
        else:
            http.handle_request(conn_from_proxy, conn_from_browser, decoded_request)
        
        conn_from_proxy.close()
        conn_from_browser.close()
        sys.exit(0)
            
    except socket.error:
        print(server_host_name)
        print(server_port)
        if conn_from_proxy:
            conn_from_proxy.close()
        if conn_from_browser:
            conn_from_browser.close()
        sys.exit(1)

