import socket

LOCAL_HOST = '127.0.0.1'

class Client():
    
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, message, port_destination):
        self.client.connect((LOCAL_HOST, port_destination))
        self.client.send(message.encode('utf-8'))
