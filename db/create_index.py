import logging

from . import dbutils


logger = logging.getLogger(__name__)

_statements = {
    'business': '''
        alter table business
        add primary key (business_id);
    ''',
    'user': '''
        alter table user
        add primary key (user_id);
    ''',
    'tip': '''
        alter table tip
        add primary key (business_id, user_id, date);
    ''',
    'review': '''
        alter table review
        add primary key (review_id);
    '''
}


def create(table):
    if table not in _statements:
        raise Exception('Table {} is not in db'.format(table))
    logger.debug('creating index for {}'.format(table))
    dbutils.execute(_statements[table])


def create_all():
    for k in _statements.keys():
        create(k)
