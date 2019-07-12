import os
from abc import ABCMeta, abstractmethod
import json


class Bridge(object):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    computers = []

    def run(self) -> None:
        for send_computer in self.computers:
            if send_computer.has_message_to_send():
                message = send_computer.send()
                received_computer = eval(message['receive'])
                received_computer.receive(message)
                if received_computer.is_received():
                    send_computer.delete_sended_message()


class Computer(metaclass=ABCMeta):

    def __init__(self) -> None:
        self.send_dir = os.path.join(self.dir_, 'Send')
        self.file_to_send = os.path.join(self.send_dir, 'message.json')
        self.receive_dir = os.path.join(self.dir_, 'Receive')
        self.file_to_receive = os.path.join(self.receive_dir, 'message.json')
        self.received = False # instance received message successfully

    def has_message_to_send(self) -> bool:
        return os.path.isfile(self.file_to_send)

    def send(self) -> str:
        with open(self.file_to_send, 'r') as file:
            sended_message = file.read()
        return json.loads(sended_message)

    def delete_sended_message(self) -> None:
        os.remove(self.file_to_send)

    def receive(self, message: str) -> None:
        with open(self.file_to_receive, 'w+') as file:
            file.write(json.dumps(message))
        self.received = True

    def is_received(self) -> bool:
        return self.received

    def write(self, message) -> None:
        with open(self.file_to_send, 'w+') as file:
            file.write(json.dumps(message))


class Computer161(Computer):
    _current_dir = os.path.dirname(os.path.realpath(__file__))
    dir_ = os.path.join(_current_dir, r'161')
    

class Computer190(Computer):
    _current_dir = os.path.dirname(os.path.realpath(__file__))
    dir_ = os.path.join(_current_dir, r'190')


if __name__ == '__main__':
    bridge = Bridge()
    computer_161 = Computer161()
    computer_190 = Computer190()
    computer_161.write(message={'receive': 'computer_190', 'data': 'Hello!'})
    computer_190.write(message={'receive': 'computer_161', 'data': 'Hi!'})
    bridge.computers.extend([computer_161, computer_190])
    bridge.run()