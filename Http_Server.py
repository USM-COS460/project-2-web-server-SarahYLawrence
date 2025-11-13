import socket
from threading import Thread
import os
from datetime import datetime,timezone
import mimetypes
import sys

def file_type(file_path):
    file_type,_ = mimetypes.guess_type(file_path)
    return file_type or "text/plain"

def current_datetime():
    current_date_time = datetime.now(timezone.utc)
    current_date_time = current_date_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return current_date_time
     
def responce_codes(http_status,content,file_path):
    current_dateandtime = current_datetime()
    current_file_type = file_type(file_path)
    length_content = len(content)
    
    match http_status:
        # Success Case
        case 200:
            responce_header = (
                "HTTP/1.1 200 OK\r\n"
            )
        # Error Case
        case 404:
            responce_header = (
            "HTTP/1.1 404 Not Found\r\n"
            )
        # Method Not Allowed Case
        case 405:
            responce_header = (
            "HTTP/1.1 405 Method Not Allowed\r\n"
            )
        # Unknown Case
        case _: 
            print("Unknown status")
   
    # Full header
    responce_header +=  ("Server: AlsToyBarn/1.0\r\n"
            f"Date: {current_dateandtime}\r\n"
            f"Content-Type: {current_file_type}\r\n"
            f"Content-Length: {length_content}\r\n"
            "\r\n")  
       
    return responce_header

def open_file(file_path):
    if os.path.isfile(file_path):
        # Reading the file bytes
        with open(file_path, 'rb') as f:
                    content = f.read()
        return content
    else:
        return b""

def parsing_file(line):
    # Parsing file path from request command
    data = line.splitlines()[0].split(' ')
    if len(data) >= 2:
        site_path = data[1]
        site_path = site_path.lstrip("/")
    else:
        site_path = ""
    
    return site_path

def file_path(line):
    # Document root form command line
    root_path = sys.argv[1]
    root_path = root_path.lstrip("/")
    # Orgnizing file path
    directory_path = os.path.dirname(os.path.abspath(__file__)) 
    site_path = parsing_file(line)    
    file_path = os.path.join(directory_path,root_path,site_path)
    return file_path

def responce(line):
    # Error content defalt 
    content = b""
    # Checking the request type
    if line.startswith("GET"):
            full_file_path = file_path(line)   
            # Getting content from file
            if os.path.isfile(full_file_path):
                content = open_file(full_file_path)
                if not content:
                    return content,responce_codes(404,content,"")
                else:
                    return content,responce_codes(200,content,full_file_path)
            else:
                return content,responce_codes(404,content,"")
    else:
        return content,responce_codes(405,content,"")

def request(conn):
        # Get request
        try:
            data = conn.recv(1024)
            if not data:
                conn.close()
            else:
                # Get responce from request
                line = data.decode('utf-8')
                content, response = responce(line) 
                # Send responce
                try:
                    conn.sendall(response.encode('utf-8') + content)
                    conn.close()
                except (OSError):
                    conn.close()
        except ConnectionResetError:
            conn.close()

  
def main():
    # Comandline args check 
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <document_root> <port>")
        sys.exit(1)

    # Server Listner
    host = 'localhost'
    port = int(sys.argv[2])


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