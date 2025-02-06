# Created by Grace Li & Kamryn Ohly
# import http.server
# import socketserver

# # Set up server
# # NOTE: check about hard-coding PORT for sanity reasons later
# PORT = 8000
# Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("Serving at port", PORT)
#     httpd.serve_forever()

# # todo: create set of active connection

# # todo: type hint this (and all) function
# def accept_connections():
#     pass

# def service_connections():
#     pass 


# import socket

# # Create a socket object
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Get the hostname of the machine
# hostname = socket.gethostname()

# # Get the IP address corresponding to the hostname
# IP_address = socket.gethostbyname(hostname)

# # Define the port on which the server will listen for connections
# port = 5000

# # Bind the socket to the IP address and port
# server_socket.bind((IP_address, port))

# # Listen for incoming connections (maximum of 5)
# server_socket.listen(5)

# print(f"Server listening on {IP_address}:{port}")

# while True:
#     # Accept a connection from a client
#     client_socket, client_address = server_socket.accept()
#     print(f"Connection from {client_address}")

#     # Receive data from the client
#     data = client_socket.recv(1024)
#     print(f"Received: {data.decode()}")

#     # Send a response to the client
#     message = "Hello from the server!"
#     client_socket.send(message.encode())

#     # Close the client socket
#     client_socket.close()


# From Lecture

import socket
import selectors
import types

selector = selectors.DefaultSelector()

hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname) 

PORT = 5000 # todo: check about if this is allowed!!


def accept_connection(sock):
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    selector.register(conn, events, data=data)

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            selector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            return_data = "data!!"
            return_data = return_data.encode("utf-8")
            sent = sock.send(return_data)
            data.outb = data.outb[sent:]

if __name__ == "__main__":
    # AF_INET defines the address family (ex. IPv4)
    # SOCK_STREAM defines socket type (ex. TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Listening on", (HOST, PORT))
    # Allow the socket to continue working without putting other possible connections on hold.
    server_socket.setblocking(False)
    # Register the initial socket by the server (only looks for incoming connections)
    selector.register(server_socket, selectors.EVENT_READ, data=None)
    try:
        # Infinitely listen to the socket
        while True:
            # Look at all currently registered sockets, and if we get an event sent, it selects it & then we handle the events.
            events = selector.select(timeout=None)
            print("events: ", events)
            for key, mask in events:
                if key.data is None:
                    accept_connection(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Caught keyboard interrupt, exiting")
    finally:
        selector.close()
