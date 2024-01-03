import os

class SocketConfig:
    sadf = 5
    afgd = 5

# class DbConfig:
#     HOST = None
#     PORT = None
#     USERNAME = None
#     PASSWORD = None


GOOGLE_KEY = None

IP = os.getenv("SERVER_IP_ADDRESS", "127.0.0.1")
PORT = os.getenv("SERVER_PORT")
HEADER_LENGTH = os.getenv("SERVER_HEADER_LENGTH")