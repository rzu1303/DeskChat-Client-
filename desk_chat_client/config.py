import os
from desk_chat_client import version


PROJECT_VERSION = version.__version__

# class DbConfig:
#     HOST = None
#     PORT = None
#     USERNAME = None
#     PASSWORD = None

GOOGLE_KEY = None

IP = os.getenv("SERVER_IP_ADDRESS", "127.0.0.1")
PORT = int(os.getenv("SERVER_PORT"))
HEADER_LENGTH = int(os.getenv("SERVER_HEADER_LENGTH"))