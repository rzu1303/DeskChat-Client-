from collections.abc import Callable, Iterable, Mapping
import sys
import time
import logging
import logging.config
from typing import Any
from PyQt5 import QtWidgets 
from threading import Thread

from desk_chat_client.views.dashboard import Dashboard
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

def start_client():
    """
    Starting the client
    """

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()

    dashborad_model = DashboardModel()
    dashboard = Dashboard(MainWindow, dashborad_model)

    MainWindow.show()

    

    dashborad_model.message_box_text = ""
    dashborad_model.new_message = "messages are here"

    t = Test(dashborad_model)
    t.start()
    sys.exit(app.exec())   


class Test(Thread):
    def __init__(self, model) -> None:
        super().__init__()

        self._model = model
        self.setDaemon(True)

    def run(self):
        # for index in range(1, 100):
        #     time.sleep(2)
        #     self._model.new_message = "kjlhdf cadh {}".format(index)
        # for index in range(1, 100):
        #     self._model.new_message = self._model.message_box_text
        if len(self._model.message_box_text) != 0:
            self._model.new_message = self._model.message_box_text

        # pass