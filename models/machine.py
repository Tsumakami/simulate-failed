import logging, time
from .client import Client
from .server import Server

TIMEOUT = 2
MAX_EXECUTION = 10

class Machine():
    client: Client
    server: Server
    name: str
    slave_port: int
    
    def __init__(self, name, port, slave_port):
        self.name = name
        self.server = Server(port, name)
        self.client = Client()
        self.slave_port = slave_port

    def get_server(self) -> Server:
        return self.server

    def get_client(self) -> Client:
        return self.client

    def task(self):
        self.executing_task = True

        count = 0
                
        logging.info(f'{self.name} - Executing task.')

        while count <= MAX_EXECUTION:
            time.sleep(TIMEOUT)
            print(f'{self.name} - TRABALHANDO...')                        

            count = count + 1

        self.executing_task = False

        raise Exception('Falha Forçada.')

    def execute_machine(self):
        pass
