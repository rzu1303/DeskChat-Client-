from desk_chat_client.views.pages.dashboard import Ui_MainWindow
import sys, os
import sys
import logging
from pprint import pprint
import datetime 
from queue import Queue
from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QListWidgetItem
from desk_chat_client import config
from desk_chat_client.views.models.dashboard import Dashboard as DashboardModel


logger = logging.getLogger(__name__)

class Dashboard(Ui_MainWindow):
    students = {}
    def __init__(self, MainWindow, model: DashboardModel = None):
        """MainWindow constructor"""
        super().setupUi(MainWindow) 

        self._model: DashboardModel = model

        # messege send
        # self.pushButton_send.clicked.connect(self.save_student)

        self._model.message_box_update.connect(self.update_message_box)
        self._model.new_message_update.connect(self.append_new_message)
        self.pushButton_send.clicked.connect(self.send_message)
    
    def send_message(self):
        self._model.new_message = self.lineEdit_message_box.text()
        self._model.input_message.put(self.lineEdit_message_box.text())
        self.lineEdit_message_box.clear()

    def show_message(self):
        self._model.new_message = self._model.recieved_messages.get()

    def update_message_box(self, message: str) -> None:
        self.lineEdit_message_box.setText(message)

    def append_new_message(self, new_message: str) -> None:
        item = QListWidgetItem(new_message, self.listWidget_message)
        self.listWidget_message.addItem(item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()

    ui = Dashboard(MainWindow)

    MainWindow.show()

    sys.exit(app.exec())    