import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

def send_request(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_s:
        client_s.connect((host, port))
        client_s.send(request)
        client_s.shutdown(socket.SHUT_WR)
        chunk = client_s.recv(BYTES_TO_READ)
        result = b'' + chunk

        while(len(chunk) > 0):
            chunk = client_s.recv(BYTES_TO_READ)
            result += chunk
        client_s.close()
        return result

def handle_conn(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        request = b""
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
            response = send_request("www.google.com", 80, request)
            conn.sendall(response)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.listen(2)

        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_conn, args=(conn, addr))
            thread.run()

start_server()