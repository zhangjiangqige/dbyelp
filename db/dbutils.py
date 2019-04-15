import logging

import pymysql


logger = logging.getLogger(__name__)


connection = None

def connect_db(host, user, password, db):
    global connection
    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)
        logger.info('Connected to database')
    except Exception as e:
        logger.exception(
            'Failed to connect to database. Exception: {}'.format(e))
        raise e


def exists(model, query):
    res = model.objects.raw(query)
    return res.count() != 0


def filter_fields(obj, fields):
    return {f: getattr(obj, f) for f in fields}
