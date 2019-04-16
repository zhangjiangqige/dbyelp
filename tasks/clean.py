from db import dbutils

# Each entry is a fix that may need to be used for the db to work properly
# e.g. create index
fixes = {
    'tip-dup-entry': {
        'description': '123',
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
