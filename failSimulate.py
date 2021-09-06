import threading, time, socket, logging
from models.client import Client
from models.server import Server
from models.machine import Machine

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='logs/tome_falha.log', encoding='utf-8', level=logging.DEBUG)

TIMEOUT = 2

MASTER_PORT = 7300
SLAVE_PORT = 7380

    
class MasterMachine(Machine):

    def execute_machine(self):
        try:    
            self.get_server().start_socket()
    
            self.task()
               
        except Exception as e:
            logging.error(f'{self.name} - Fail on execution. Error={e}')
            
            self.get_client().send_message('FAILED', self.slave_port)
                   
            self.get_server().disconnect()

           
class SlaveMachine(Machine):
    
    def execute_machine(self):
        try:    
            self.get_server().start_socket()

            while True:
                logging.debug(f'{self.name} - listen message.')
            
                resp = self.get_server().recv_message(1024)
                
                if resp == 'FAILED':
                    self.task()
                    break
    
        except Exception as e:
            logging.error(f'{self.name} - Fail on execution. error={e}')
            
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
