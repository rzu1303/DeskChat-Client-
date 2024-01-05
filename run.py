import sys
import os
import logging
import datetime
import argparse

from desk_chat_client.services import setup, start_client


logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Update inventory in acenda.')
    setup()

    start_client()


if __name__ == "__main__":
    main()