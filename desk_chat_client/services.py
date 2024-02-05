from collections.abc import Callable, Iterable, Mapping
import sys
import time
import logging
import logging.config
from typing import Any
from PyQt5 import QtWidgets 
from threading import Thread
import threading
import socket
import errno
from queue import Queue
from desk_chat_client import config

from desk_chat_client.views.dashboard import Dashboard
from desk_chat_client.views.models.dashboard import DASHBOARD_MODEL
from desk_chat_client.views.models.dashboard import Dashboard as DashboardModel

logger = logging.getLogger(__name__)


def setup():
    """
    Set up configuration and logging
    """

    from desk_chat_client.logger import LOGGING

    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )

    logging.config.dictConfig(LOGGING)

    return

def update_server_ip(server_ip):    
    if server_ip != None:
        parts = server_ip.split(":")

        config.IP = parts[0]
        config.PORT = int(parts[1])
        logging.info("Server IP = {config.IP} at server PORT = {config.PORT}")



def start_client():
    """
    Starting the client
    """

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()

    dashboard = Dashboard(MainWindow, DASHBOARD_MODEL)

    MainWindow.show()
    
    DASHBOARD_MODEL.message_box_text = "Enter username"
    DASHBOARD_MODEL.new_message = "messages are here"

    connection_thread = ClientServerConnection(DASHBOARD_MODEL)
    connection_thread.start()
    
    sys.exit(app.exec())   


class ClientServerConnection(Thread):
    def __init__(self, model):
        super().__init__()
        # self._lock = threading.Lock()

        self.client_socket = None
        self.username = None
        self._model: DashboardModel = model
        self.IP = config.IP
        self.PORT = config.PORT
        self.HEADER_LENGTH = config.HEADER_LENGTH 
        self.setDaemon(True)


    def send_message(self, message):
        message = message.encode('utf-8')
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(message_header + message)


    def receive_messages(self):
        while True:
            try:
                username_header = self.client_socket.recv(self.HEADER_LENGTH)

                if not len(username_header):

                    logging.info("Connection Has been lost from server")

                    sys.exit()

                username_length = int(username_header.decode('utf-8').strip())
                other_username = self.client_socket.recv(username_length).decode('utf-8')

                message_header = self.client_socket.recv(self.HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())

                recieved_message = self.client_socket.recv(message_length).decode('utf-8')
                message =  other_username + ' : ' + recieved_message

                self._model.recieved_messages.put(message)
                self._model.new_message = self._model.recieved_messages.get()


            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    sys.exit()


    def run(self):     
        while True:
            if not self._model.input_message.empty():
                self.username = self._model.input_message.get()
                break
            time.sleep(0.2)

        logging.info("Listening for connections on IP = {} at PORT = {}".format(config.IP, config.PORT))
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.IP, self.PORT))
        self.client_socket.setblocking(False)
        self.client_socket.send(f"{len(self.username):<{self.HEADER_LENGTH}}".encode('utf-8') + self.username.encode('utf-8'))
        # receive_thread = threading.Thread(target=self.receive_messages, args=())
        # receive_thread.start() 
       
        while True:
            message = self._model.input_message.get()
            if message:
                self.send_message(message) 
            
            self.receive_messages()
