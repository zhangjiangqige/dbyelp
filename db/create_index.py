import logging

from . import dbutils


logger = logging.getLogger(__name__)

_statements = {
    'business_train': 'alter table business_train add index (business_id)',
    'business_val': 'alter table business_val add index (business_id)',
    'user': 'alter table user add index (user_id)',
    'review_train': '''
        alter table review_train add index (business_id);
        alter table review_train add index (user_id);
    ''',
    'review_val': '''
        alter table review_val add index (business_id);
        alter table review_val add index (user_id);
    '''
}


def create(table):
    if table not in _statements:
        raise Exception('Table {} is not in db'.format(table))
    logger.debug('creating index for {}'.format(table))
    for s in _statements[table].split(';'):
        if len(s.strip()) > 0:
            dbutils.execute(s, print=True)


def create_all():
    for k in _statements.keys():
        create(k)
