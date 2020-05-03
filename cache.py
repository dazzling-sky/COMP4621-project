import json
import uuid
import os

def is_required(decoded_request):
    request_parts = decoded_request.split('\n')
    for i in range(len(request_parts)):
        if request_parts[i].startswith('Cache-Control'):
            cache_setting = request_parts[i].split(':')[1].strip()
            if cache_setting == 'no-cache':
                return False
            else:
                break
    
    return True

def write_cache(decoded_request, response, lock):
    cache_json = None

    lock.acquire()
    cache_json_read_file = open("cache.json", "r")
    cache_json = json.load(cache_json_read_file)

    server_url = decoded_request.split(' ')[1]
    filename = cache_json.get(server_url)

    if filename is None:
        #Generate a new file name
        filename = uuid.uuid4().hex
        cache_json[server_url] = filename
        cache_json_write_file = open("cache.json", "w")
        json.dump(cache_json, cache_json_write_file)
    
    lock.release()
    path = cur_path()

    cache_write = open(path + "/cache" + "/" + filename, "ab")
    cache_write.write(response)

def cur_path():
    return os.getcwd()


def cache_exists(server_url):
    cache_json_read_file = open("cache.json", "r")
    cache_json = json.load(cache_json_read_file)

    if cache_json.get(server_url):
        return True
    
    return False

def return_data(server_url):
    cache_json_read_file = open("cache.json", "r")
    cache_json = json.load(cache_json_read_file)

    unique_id = cache_json.get(server_url)
    if not unique_id:
        return

    path = cur_path()
    cache_read = open(path + "/cache" + "/" + unique_id, "rb")
    return cache_read.read()