from PyQt5.QtCore import QObject, pyqtSignal
from queue import Queue

class Dashboard(QObject):
    message_box_update = pyqtSignal(str)
    new_message_update = pyqtSignal(str)
    

    @property
    def message_box_text(self) -> str:
        # self.temp_message_box_text = self._message_box_text
        # self._message_box_text = ""
        # return self.temp_message_box_text
        return self._message_box_text
    
    @message_box_text.setter
    def message_box_text(self, value: str):
        # updating message in GUI
        self.message_box_update.emit(value)
        self._message_box_text = value

    @property
    def new_message(self) -> str:
        return self._new_message
    
    @new_message.setter
    def new_message(self, value: str):
        # updating message in GUI
        self.new_message_update.emit(value)
        self._new_message = value


    def __init__(self):
        super().__init__()

        self._message_box_text = ""
        self._new_message = ""
        self.input_message = Queue()
        self.recieved_messages = Queue()

        
DASHBOARD_MODEL = Dashboard()


    