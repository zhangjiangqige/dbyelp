import logging
import sys

from dbyelp import init
from app import app
from utils import config


if __name__ == '__main__':
    init()

    host = config.conf['host']
    port = config.conf['port']
    logging.info('Server listening on {}:{}'.format(host, port))
    import views
    app.run(threaded=True, host=host, port=port)
