from desk_chat_client.views.pages.dashboard import Ui_MainWindow
import sys, os
import sys
import logging
from pprint import pprint
import datetime 
from queue import Queue
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QLabel, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtWidgets import QListWidgetItem
from desk_chat_client import config
from desk_chat_client.views.models.dashboard import Dashboard as DashboardModel


logger = logging.getLogger(__name__)


class CustomItemWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        
        # self.label = QLabel(text)

        # self.label.setWordWrap(True)
                
        # self.label.setMinimumWidth(50)  # Set the desired fixed width(No)
        # self.label.setMaximumWidth(400)  # Set the desired fixed width
        # self.label.setMinimumHeight(50)  # Set the desired fixed width
        # self.label.setMaximumHeight(500)  # Set the desired fixed width
        # self.label.setAlignment(Qt.AlignVCenter)

        # layout = QGridLayout(self)
        # layout.addWidget(self.label)

        # layout.setAlignment(self.label, Qt.AlignVCenter)
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)

        min_width = 100
        max_width = 500
        min_height = 100
        max_height = 500
        self.text_edit.setMinimumWidth(min_width)
        self.text_edit.setMaximumWidth(max_width)
        self.text_edit.setMinimumHeight(min_height)
        self.text_edit.setMaximumHeight(max_height)
        
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        
        layout.addWidget(self.text_edit)

        # layout.addStretch()
        # layout.addWidget(self.label)
    def resizeEvent(self, event):
        # Adjust the size dynamically based on the content size and within min and max height
        print("herefgfsdgs bdf")
        content_size = self.text_edit.document().size().toSize()
        adjusted_height = min(max(content_size.height(), self.text_edit.minimumHeight()), self.text_edit.maximumHeight())
        self.text_edit.setMaximumHeight(adjusted_height)

        adjusted_width = min(max(content_size.width(), self.text_edit.minimumWidth()), self.text_edit.minimumWidth())
        self.text_edit.setMaximumWidth(adjusted_width)

        super().resizeEvent(event)



class Dashboard(Ui_MainWindow):
    def __init__(self, MainWindow, model: DashboardModel = None):
        """MainWindow constructor"""
        super().setupUi(MainWindow) 

        self._model: DashboardModel = model

        self._model.message_box_update.connect(self.update_message_box)
        self._model.new_message_update.connect(self.append_new_message)

        self.pushButton_send.clicked.connect(self.send_message)
        self.lineEdit_message_box.returnPressed.connect(self.send_message)

        # self.lineEdit_message_box.clicked.connect(self.message_box_clear)
        # self.lineEdit_message_box.mousePressEvent.connect(self.message_box_clear)

        print("MainWindow size policy:", MainWindow.sizePolicy())
        print("MainWindow size policy: ", MainWindow.sizePolicy().horizontalPolicy(), MainWindow.sizePolicy().verticalPolicy())

    def scroll_to_bottom(self):
        # Scroll to the bottom of the listWidget_message
        self.listWidget_message.scrollToBottom()
    
    def message_box_clear(self):
        self.lineEdit_message_box.clear()

    
    def send_message(self):
        self._model.new_message = self.lineEdit_message_box.text()
        self._model.input_message.put(self.lineEdit_message_box.text())
        self.message_box_clear()
        self.scroll_to_bottom()

    def show_message(self):
        self._model.new_message = self._model.recieved_messages.get()

    def update_message_box(self, message: str) -> None:
        self.lineEdit_message_box.setText(message)

    def append_new_message(self, new_message: str) -> None: 
        # item = QListWidgetItem(new_message, self.listWidget_message)
        # self.listWidget_message.addItem(item)
        item_widget = CustomItemWidget(new_message, parent=self.listWidget_message)

        item = QListWidgetItem()

        # item.setSizeHint(item_widget.sizeHint())
        item.setSizeHint(item_widget.text_edit.sizeHint())
        self.listWidget_message.addItem(item)
        self.listWidget_message.setItemWidget(item, item_widget)
        self.scroll_to_bottom()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()

    ui = Dashboard(MainWindow)

    MainWindow.show()

    sys.exit(app.exec())    