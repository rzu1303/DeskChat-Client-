import sys
import os
import logging
import datetime

from desk_chat_client.services import setup, start_client


logger = logging.getLogger(__name__)

def main():
    setup()

    start_client()


if __name__ == "__main__":
    main()