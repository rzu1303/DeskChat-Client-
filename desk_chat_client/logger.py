import os
import sys

PROJ_ROOT_DIR = os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))

LOG_DIR = os.getenv('LOG_DIR', PROJ_ROOT_DIR + '/logs')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            ' %(levelname)s %(asctime)s %(process)d %(thread)d [%(name)s] '+' %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/desk_chat_client.log',
            'maxBytes': 1048576,
            'backupCount': 3
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        'py.warnings': {
            'level': 'ERROR'
        }

    },
}