from db import dbutils

# Each entry is a fix that may need to be used for the db to work properly
# e.g. create index
fixes = {
    'tip-dup-entry': {
        'description': 'There exists rows with identical values in the table tip. This job de-duplicates them.',
        'statement': '''
            create table `tip_fix_tip-dup-entry` (
                business_id char(32) not null,
                compliment_count int default 0,
                date datetime not null,
                user_id char(32) not null
            );
            insert into `tip_fix_tip-dup-entry` (
                select *
                from tip
                group by business_id, user_id, date
            );
            alter table `tip_fix_tip-dup-entry` add primary key (business_id, user_id, date);
            drop table tip;
            rename table `tip_fix_tip-dup-entry` to tip;
        '''
    },
    'review-dup-entry': {
        'description': 'There exists rows with identical values in the table review. This job de-duplicates them.',
        'statement': '''
            create table `review_fix_review-dup-entry` (
                business_id char(32) not null,
                cool int default 0,
                date datetime not null,
                funny int default 0,
                review_id char(32) not null,
                stars int default 0,
                useful int default 0,
                user_id char(32) not null
            );
            insert into `review_fix_review-dup-entry` (
                select *
                from review
                group by review_id
            );
            alter table `review_fix_review-dup-entry` add primary key (review_id);
            drop table review;
            rename table `review_fix_review-dup-entry` to review;
        '''
    }
}


def clean_list():
    return fixes


def clean(name):
    if name not in fixes:
        return
    fix = fixes[name]
    dbutils.execute(fix['statement'])


def restore(table):
    with open('sql/tables/{}.sql'.format(table)) as f:
        stmt = f.read()
    dbutils.execute('''
        drop table {};
        {};
        insert into {} (select * from {}_ori);
    '''.format(table, stmt, table, table))
