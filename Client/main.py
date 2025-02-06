import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port
# todo: how to not hard-code this???
PORT = 5000
server_address = ("10.250.29.158", PORT)

# Connect to the server
client_socket.connect(server_address)

# Send data to the server
message = "Hello from the client!"
client_socket.send(message.encode())

# Receive data from the server
data = client_socket.recv(1024)
print(f"Received: {data.decode()}")

while True:
    print("")

# Close the socket
# client_socket.close()