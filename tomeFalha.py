import threading, time, socket, logging
from message_channel import Channel
from client import Client
from server import Server

logging.basicConfig(filename='tome_falha.log', encoding='utf-8', level=logging.DEBUG)

TIMEOUT = 2
MAX_REQUESTS = 15
LOCAL_HOST = '127.0.0.1' 
MAX_EXECUTION = 50

MASTER_PORT = 7300
SLAVE_PORT = 7380

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
        count = 0
                
        logging.info(f'{self.name} - Executing print_state_machine.')

        while count <= MAX_EXECUTION:
            print(f'{self.name} - TRABALHANDO...')                        

            count = count + 1

        raise ValueError('Falha na Execução.')

    def execute_machine(self):
        pass
    
class MasterMachine(Machine):

    def execute_machine(self):
        try:    
            self.get_server().start_socket()
    
            self.task()
               
        except ValueError:
            logging.error(f'{self.name} - Fail on execution.')
            time.sleep(TIMEOUT) 
            self.get_client().send_message('FAILED', self.slave_port)
            resp = self.get_server().recv_message(1024)
        
            print(f'{self.name} - resp={resp}') 
            self.get_server().disconnect()
        
class SlaveMachine(Machine):
    def execute_machine(self):
        try:    
            self.get_server().start_socket()
            resp = self.get_server().recv_message(1024)

            while resp != 'FAILED':
                print(f'{self.name} - ESPERANDO...')                
            self.task()

        except ValueError:
            logging.error(f'{self.name} - Fail on execution.')
            self.get_client().send_message('FAILED', self.slave_port)
            self.get_server().disconnect()
            
def execute_thread(index: int, machine: Machine):
    thread = threading.current_thread()
    logging.info(f'{thread.name} - Start thread.')

    machine.execute_machine()

if  __name__ == "__main__" :
    master = MasterMachine('Master', MASTER_PORT, SLAVE_PORT)    
    slave = SlaveMachine('Slave', SLAVE_PORT, MASTER_PORT)

    threadMaster = threading.Thread(target=execute_thread, name="Master", args=(0, master))
    threadSlave = threading.Thread(target=execute_thread, name="Slave", args=(1, slave))
    
    threadMaster.start()
    threadSlave.start()
    
    master.get_server().disconnect()
    slave.get_server().disconnect()
        
