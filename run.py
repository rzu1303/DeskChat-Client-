import sys

import logging
import argparse

from desk_chat_client.services import setup, start_client, update_server_ip
from desk_chat_client import config

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Start DeskChat Client')
    parser.add_argument('-s', nargs=1, help='Give Server IP:PORT')
    
    args = parser.parse_args()

    server_address = args.s[0] if args.s is not None and len(
        args.s) > 0 else None

    update_server_ip(server_address)

    setup()

    logger.info("Starting DeskChat version %s",config.PROJECT_VERSION)

    try:
        start_client()
    except:
        logging.exception('')
        sys.exit(1)


if __name__ == "__main__":
    main()