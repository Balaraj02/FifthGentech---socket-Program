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

# Server class
class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.protocol_handlers = {}
    
    def add_protocol_handler(self, protocol_name, handler):
        self.protocol_handlers[protocol_name] = handler
    
    def handle_client(self, connection, address):
        print(f"Connected by {address}")
        protocol_handler = self.protocol_handlers['example']  # Example usage
        while True:
            try:
                # Read from the client
                data = protocol_handler.read(connection)
                if not data:
                    break
                # Process the data (echo in this case)
                response = f"Echo: {data}"
                # Write back to the client
                protocol_handler.write(connection, response)
            except Exception as e:
                print(f"Error: {e}")
                break
        connection.close()
        print(f"Disconnected from {address}")
    
    def start(self):
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.ip}:{self.port}")
        while True:
            connection, address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
            client_thread.start()

# Unit Test
def unit_test():
    server = Server('localhost', 9999)
    server.add_protocol_handler('example', ExampleProtocolHandler())
    server_thread = threading.Thread(target=server.start)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server a moment to start
    import time
    time.sleep(1)
    
    # Running the test stub
    test_stub('localhost', 9999)
    print("Unit test completed")

# Test Stub
def test_stub(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    client_socket.sendall(b"Hello, Server!")
    response = client_socket.recv(1024)
    print(f"Server response: {response.decode()}")
    client_socket.close()

if __name__ == "__main__":
    unit_test()
    # Keep the main thread alive to allow server to keep running
    import time
    while True:
        time.sleep(1)
