import threading, time
from message_channel import Channel

TIMEOUT = 3

class Channel():
    sockets: List[Socket]

    def __init__(self, sockets: List[Socket]):
        self.sockets = sockets

    def send(self, origin, destination, message)
        for socket in sockets:
            if(socket.origin == origin)


class Socket():
    destination: int
    origin: int
    message: dict

    def __init__(self, destination, origin)
        self.destination
        self.origin
    





class Machine():
    
    def __init__(self, name):
        self.name = name

    def execute(self):
        pass


def execute_thread(index, message):
    thread = threading.current_thread()
    channel = Channel().open()


    is_set = switch_event.wait(4)

    if is_set:
        print('{} - threads actives: {}'.format(thread.name, is_set))

if  __name__ == "__main__" :

    switch_event = threading.Event()

    threadMaster = threading.Thread(target=execute_thread, name="Master", args=(0, "Executando a Master"))
    threadSlave = threading.Thread(target=execute_thread, name="Slave", args=(1,"Executando a Slave"))

    threadMaster.start()
    threadSlave.start()

    time.sleep(TIMEOUT)
    switch_event.set()
