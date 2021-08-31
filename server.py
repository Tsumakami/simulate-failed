import logging, socket

LOCAL_HOST = '127.0.0.1' 

class Server():
    message: dict
    port: int
    name: str    

    def __init__(self, port: int, name: str):
        self.port = port
        self.name = name
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start_socket(self):
        logging.info(f"{self.name} - Start server in host={LOCAL_HOST} porta={self.port}.")

        self.server.bind((LOCAL_HOST, self.port))

        self.server.listen()

    def recv_message(self, bytes_recv: int):
        conn, addr = self.server.accept()
        
        logging.info(f'{self.name} - conn{conn}, addr={addr}')
        
        resp = conn.recv(bytes_recv).decode()
        
        logging.info(f'{self.name} - Receiving message: {resp}')
        
        return resp

    def disconnect(self):
        self.server.close()
