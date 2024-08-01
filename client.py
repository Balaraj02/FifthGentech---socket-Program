import socket
import threading

# Protocol handler base class
class ProtocolHandler:
    def read(self, connection):
        raise NotImplementedError
    
    def write(self, connection, data):
        raise NotImplementedError

# Example protocol handler for a specific protocol
class ExampleProtocolHandler(ProtocolHandler):
    def read(self, connection):
        data = connection.recv(1024).decode()
        print(f"Read data: {data}")
        return data
    
    def write(self, connection, data):
        connection.sendall(data.encode())
        print(f"Wrote data: {data}")

class Client:
    def __init__(self, ip, port, protocol_handler):
        self.ip = ip
        self.port = port
        self.protocol_handler = protocol_handler
    
    def start(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip, self.port))
        msg = input("enter a message: ")
        # Write to the server
        self.protocol_handler.write(client_socket, msg)
        
        # Read from the server
        response = self.protocol_handler.read(client_socket)
        print(f"Server response: {response}")
        
        client_socket.close()

# Example usage
if __name__ == "__main__":
    protocol_handler = ExampleProtocolHandler()
    client = Client('localhost', 9999, protocol_handler)
    client_thread = threading.Thread(target=client.start)
    client_thread.start()
