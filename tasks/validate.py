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
        'drop table if exists business_train',
        'drop table if exists business_val',
        'create table business_train like business',
        'create table business_val like business',
        'insert into business_train (select * from business limit 100000)',
        'insert into business_val (select * from business limit 200000 offset 100000)'
    ]
    for q in queries:
        dbutils.execute(q, print=True)


def split_review():
    queries = [
        'drop table if exists review_train;',
        'drop table if exists review_val;',
        'create table review_train like review;',
        'create table review_val like review;',
        'insert into review_train (select * from review where business_id in (select business_id from business_train));',
        'insert into review_val (select * from review where business_id in (select business_id from business_val));'
    ]
    for q in queries:
        dbutils.execute(q, print=True)
