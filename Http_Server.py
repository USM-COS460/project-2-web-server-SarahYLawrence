import socket
from threading import Thread
import os
from datetime import datetime
import mimetypes
import sys

def file_type(file_path):
    file_type = mimetypes.guess_type(file_path)
    return file_type[0]

def current_datetime():
    current_datentime = datetime.now()
    current_datentime = current_datentime.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return current_datentime
     
def responce_codes(http_status,content,file_path):
    current_dateandtime = current_datetime()
    
    match http_status:
        # Success Case
        case 200:
            responce_header = (
                "HTTP/1.1 200 OK\r\n"
                "Server: AlsToyBarn/1.0\r\n"
                f"Date: {current_dateandtime}\r\n"
                f"Content-Type: {file_type(file_path)}\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
            )
        # Error Case
        case 404:
            responce_header = (
            "HTTP/1.1 404 Not Found\r\n"
            f"Date: {current_dateandtime}\r\n"
            "\r\n"
            )
        # Unknown Case
        case _: 
            print("Unknown status")
    return responce_header

def open_file(file_path):
    if os.path.isfile(file_path):
                # Reading the file bytes
                with open(file_path, 'rb') as f:
                    content = f.read()
    return content

def parsing_file(line):
    # Parsing file path from request command
    data = line.splitlines()[0].split(' ')
    if len(data) >= 2:
        site_path = data[1]
        site_path = site_path.lstrip("/")
    else:
        site_path = ""
    
    return site_path

def respons(line):
    if line.startswith("GET"):
            # Orgnizing file path
            directory_path = os.path.dirname(os.path.abspath(__file__))   
            site_path = parsing_file(line)    
            file_path = os.path.join(directory_path,site_path)
            # Getting content from file
            if os.path.isfile(file_path):
                content = open_file(file_path)
                return content,responce_codes(200,content,file_path)
            else:
                return "",responce_codes(404,"","")
    else:
        return "",responce_codes(404,"","")

def request(conn):
    while True:
        # Get request
        data = conn.recv(1024)
        line = data.decode('utf-8')
        # Get responce from request
        content, response = respons(line) 
        # Send responce
        conn.send(response.encode('utf-8'))
        if "404" in response:
            break
        else:
            conn.sendall(content)
    conn.close()

def main():
    # Comandline args check 
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <port>")
        sys.exit(1)

    # Server Listner
    host = 'localhost'
    port = int(sys.argv[1])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen()
    while True:
        client, address = sock.accept()
        client_thread = Thread(target=request, args=(client,))
        client_thread.start()


if __name__ == "__main__":
    main()