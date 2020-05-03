# COMP4621-project

Multi-threaded Proxy Server

- Name: Hyunho Kim
- Student no: 20215807
- Student ID: hhkimaa

## Getting started

Open your Proxy setting and type in proxy server setting as follows:
  - Proxy Server address: 127.0.0.1
  - Port no: 12000

## Installing

Clone this remote repository into your own local workspace by typing:
```sh
git clone https://github.com/dazzling-sky/COMP4621-project.git
```

## Running

Within the root directory, type in the command:

```sh
python3 server.py
```
The proxy server is running when an output similar to the following is displayed on the console:

```
The server is ready to receive...
```

## Requirements

  1. Multi-threaded operations:
      - Open multiple browsers and type in appropriate url to get the webpage
    
  2. HTTP requests forwarding:
      - Enter URL (e.g. http://www.apache.org)
      - Status Code can be checked with developer mode in browser
    
  3. HTTPS requests forwarding:
      - Enter URL (e.g. https://www.google.com)
      - Should successfully tunnel the request from browser to the remote server
  
  4. Access Control
      - Write any websites to be blacklisted on blacklist.txt
      - Should receive 404 error on the browser upon request
  
  5. Cacheing
      - Access any webpage that sends request with "Cache-Control" header (e.g. http://www.apache.org)
      - Check cache.json to see if the url is appropriately mapped to a unique id
      - Check if contents are properly stored within **/cache** directory
