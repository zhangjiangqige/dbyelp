import sys

from db import dbutils
from utils import config


def init():
    if len(sys.argv) == 1:
        print('args: config_file')
        exit(0)

    config.initialize(sys.argv[1])
    dbutils.connect_db(
        config.conf['db_host'],
        config.conf['db_user'],
        config.conf['db_password'],
        config.conf['db_db'])
