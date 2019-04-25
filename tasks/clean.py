import logging

from db import dbutils


logger = logging.getLogger(__name__)


# Each entry is a fix that may need to be used for the db to work properly
# e.g. create index
fixes = {
    'tip-dup-entry': {
        'description': 'There exists rows with identical values in the table tip. This job de-duplicates them.',
        'statements': [
            '''create table `tip_fix_tip-dup-entry` (
                business_id char(32) not null,
                compliment_count int default 0,
                date datetime not null,
                user_id char(32) not null
            );''',
            '''insert into `tip_fix_tip-dup-entry` (
                select *
                from tip
                group by business_id, user_id, date
            );''',
            'drop table tip;',
            'rename table `tip_fix_tip-dup-entry` to tip;'
        ]
    },
    'remove-user-with-wrong-avg-star': {
        'description': 'Some users have an average star with a large difference between the star calculated from the table review. This fix removes these kind of user from the tables user and review.',
        'statements_prepare': [
            'drop table if exists user_with_wrong_average_stars;',
            '''
            create table user_with_wrong_average_stars (
                user_id char(32) not null,
                average_stars float default 0,
                review_avg_stars float default 0
            );''',
            '''
            insert into user_with_wrong_average_stars (
                select user.user_id, user.average_stars, rev.a_star
                from user inner join
                (select user_id, avg(stars) as a_star
                from review group by user_id) as rev
                on user.user_id = rev.user_id
                where abs(user.average_stars - rev.a_star) > 1
            );
            ''',
        ],
        'statements': [
            '''
            create table user_tmp (
                average_stars float default 0,
                cool int default 0,
                elite VARCHAR(1024) default null,
                fans int default 0,
                review_count int default 0,
                useful int default 0,
                user_id char(32) not null,
                yelping_since datetime
            );''',
            '''
            insert into user_tmp (
                select * from user where user_id not in (select user_id from user_with_wrong_average_stars)
            );''',
            'drop table user;',
            'rename table user_tmp to user;',
            '''
            create table review_tmp (
                business_id char(32) not null,
                cool int default 0,
                date datetime not null,
                funny int default 0,
                review_id char(32) not null,
                stars int default 0,
                useful int default 0,
                user_id char(32) not null
            );''',
            '''insert into review_tmp (
                select * from review where user_id not in (select user_id from user_with_wrong_average_stars)
            );''',
            'drop table review;',
            'rename table review_tmp to review;'
        ]
    }
}


def clean_list():
    return fixes


def clean(name):
    if name not in fixes:
        return
    logger.info('running clean task {}'.format(name))
    fix = fixes[name]
    if 'statements_prepare' in fix:
        for s in fix['statements_prepare']:
            dbutils.execute(s)
    for s in fix['statements']:
        dbutils.execute(s)


def restore(tables=['business', 'review', 'tip', 'user']):
    for t in tables:
        logger.info('restoring {}'.format(t))
        with open('sql/tables/{}.sql'.format(t)) as f:
            stmt = f.read()
        queries = '''
            drop table if exists {};
            {};
            insert into {} (select * from {}_ori);'''.format(t, stmt, t, t).split(';')
        for q in queries:
            if q:
                dbutils.execute(q)
