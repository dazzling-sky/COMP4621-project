import socket
import sys
import cache
import threading

LOCK = threading.Lock()

def handle_request(conn_from_proxy, conn_from_browser, decoded_request):

    is_cache_required = cache.is_required(decoded_request)

    original_request = modify_http_request(decoded_request)
    send_request_as_client(conn_from_proxy, original_request)
    
    try:
        response = recv_response_from_server(conn_from_browser, conn_from_proxy, is_cache_required, decoded_request)
        conn_from_browser.send(response)
        
    except socket.error:
        pass

    sys.exit(0)

def modify_http_request(request_message):
    request_parts = request_message.split('\r\n')
    host_string = ''
    for i in range(len(request_parts)):
        if request_parts[i].startswith('Host: '):
            host_name_index = request_parts[i].find('Host: ') + len('Host: ')
            host_string = 'http://%s' % request_parts[i][host_name_index:].strip()
            continue
        
        if request_parts[i].startswith('Proxy-Connection: '):
            request_parts[i] = request_parts[i].replace('Proxy-Connection', 'Connection')
            continue
        
    for i in range(len(request_parts)):
        if request_parts[i].startswith('Accept-Encoding: '):
            request_parts.pop(i)
            break
    
    for i in range(len(request_parts)):
        if request_parts[i].startswith('Cookie: '):
            request_parts.pop(i)
            break


    split_parts = request_parts[0].split(' ')
    split_parts[1] = split_parts[1][split_parts[1].find(host_string) + len(host_string):]
    request_parts[0] = ' '.join(split_parts)

    request_message = '\r\n'.join(request_parts)
    request_message = request_message + '\r\n\r\n'

    return request_message

def send_request_as_client(proxy_as_client_socket, original_request):
    proxy_as_client_socket.sendall(bytes(original_request, 'utf-8'))

def recv_response_from_server(proxy_browser_connection, proxy_as_client_socket, is_cache_required,decoded_request):
    response = proxy_as_client_socket.recv(4096)
    if is_cache_required:  
        cache.write_cache(decoded_request, response, LOCK)

    header_body_split = response.split(b'\r\n\r\n')
    header = bytes.decode(header_body_split[0], 'utf-8')
    body = header_body_split[1]
    
    content_length = int(get_content_length(header))
    current_body_length = len(body)


    while(current_body_length < content_length):
        response = proxy_as_client_socket.recv(4096)
        if is_cache_required:
            cache.write_cache(decoded_request, response, LOCK)
        body += response
        current_body_length += len(response)
    
    header_body_split[0] = str.encode(header)
    header_body_split[1] = body
    
    proxy_as_client_socket.close()
    return b'\r\n\r\n'.join(header_body_split)

def get_content_length(response_header):
    header_parts = response_header.split('\r\n')
    length = 0
    for i in range(len(header_parts)):
        if 'Content-Length: ' in header_parts[i]:
            index = header_parts[i].find('Content-Length: ') + len('Content-Length: ')
            length = header_parts[i][index:]
            break

    return length