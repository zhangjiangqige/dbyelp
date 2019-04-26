import logging

from db import dbutils


logger = logging.getLogger(__name__)


def split_train_val():
    logger.debug('split business now')
    split_business()
    logger.debug('split review now')
    split_review()


def split_business():
    queries = [
        'drop view if exists business_train_view',
        'drop view if exists business_val_view',
        'create view business_train_view as select * from business limit 100000',
        'create view business_val_view as select * from business limit 200000 offset 100000',
    ]
    for q in queries:
        dbutils.execute(q, print=True)


def split_review():
    queries = [
        'drop view if exists review_train_view',
        'drop view if exists review_val_view',
        'create view review_train_view as select * from review where business_id in (select business_id from business_train_view)',
        'create view review_val_view as select * from review where business_id in (select business_id from business_val_view)'
    ]
    for q in queries:
        dbutils.execute(q, print=True)
