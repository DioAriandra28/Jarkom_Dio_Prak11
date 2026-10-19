import socket
import threading

connections = []
total_connections = 0

class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return f"{self.id} {self.address}"
    
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(1024)
            except:
                print(f"Client {self.address} has disconnected")
                self.signal = False
                connections.remove(self)
                break

            if data:
                message = data.decode("utf-8")
                print(f"ID {self.id}: {message}")

                # broadcast
                for client in connections:
                    if client.id != self.id:
                        client.socket.sendall(data)


def newConnections(sock):
    global total_connections
    while True:
        client_socket, address = sock.accept()
        client = Client(client_socket, address, total_connections, "Name", True)
        connections.append(client)
        client.start()
        print(f"New connection at ID {client}")
        total_connections += 1


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    thread = threading.Thread(target=newConnections, args=(sock,))
    thread.start()


main()
