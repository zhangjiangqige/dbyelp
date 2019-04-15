import json

import pymysql.cursors


# Connect to the database
connection = pymysql.connect(host='marmoset04.shoshin.uwaterloo.ca',
                             user='j892zhan',
                             password='12345678',
                             db='db356_j892zhan',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

yelp_root = '/tmp/j892zhan/workspace/yelp_dataset'


def exe(statement):
    try:
        with connection.cursor() as cursor:
            cursor.execute(statement)
        connection.commit()
    except Exception as e:
        print(statement)
        raise e


def exe_many(statements):
    n = len(statements)
    for i, s in enumerate(statements):
        if i % 10 == 0:
            print('exec_many {}/{}'.format(i, n))
        exe(s)


def create_tables():
    with open('create_tables.sql') as f:
        content = f.read()
    lines = content.replace('\n', '').split(';')
    for l in lines:
        l = l.strip()
        if l:
            print(l)
            exe(l)


def get_attrs(fn):
    attrs = []
    with open(fn) as f:
        for l in f.read().splitlines():
            a, pre, post = l.split(',')
            attrs.append((a, pre, post))
    return attrs


def get_val(j, key, default=None):
    if '__' not in key:
        return str(j.get(key, default))
    k, kk = key.split('__')
    if k not in j:
        return default
    return str(j[k].get(kk, default))


def values_batch(table, values, batch_size=100):
    ret = []
    s = 'insert into {} values '.format(table)
    i = 0
    n = len(values)
    while i < n:
        vals = values[i : i + batch_size]
        ret.append(s + ','.join(vals))
        i += batch_size
    return ret


def insert_user():
    attrs = get_attrs('attrs/filtered/user.txt')
    vals = []
    with open(yelp_root + '/user.json') as f:
        for i, l in enumerate(f):
            if i % 50000 == 0:
                print('read user {}'.format(i))
            j = json.loads(l)
            vs = [a[1] + get_val(j, a[0], '') + a[2] for a in attrs]
            vals.append('(' +  ','.join(vs) + ')')

    print('found {} users'.format(len(vals)))
    stmts = values_batch('user', vals)
    exe_many(stmts)


def insert_business():
    attrs = get_attrs('attrs/filtered/business.txt')
    vals = []
    with open(yelp_root + '/business.json') as f:
        for i, l in enumerate(f):
                if i % 50000 == 0:
                    print('read business {}'.format(i))
                j = json.loads(l)
                vs = [a[1] + get_val(j, a[0], '') + a[2] for a in attrs]
                vals.append('(' +  ','.join(vs) + ')')

    print('found {} business'.format(len(vals)))
    stmts = values_batch('business', vals)
    exe_many(stmts)

def insert_review():
    table = 'review'
    attrs = get_attrs('attrs/filtered/{}.txt'.format(table))
    vals = []
    with open(yelp_root + '/{}.json'.format(table)) as f:
        for i, l in enumerate(f):
            if i % 50000 == 0:
                print('read {} {}'.format(table, i))
            if i != 0 and i % 100000 == 0:
                stmts = values_batch(table, vals)
                exe_many(stmts)
                vals = []

            j = json.loads(l)
            vs = [a[1] + get_val(j, a[0], '') + a[2] for a in attrs]
            # vs[-3] = "'" + vs[-3][1:-1][:10].replace('"', '').replace("'", '').replace('\n',' /n ') + "'"
            vals.append('(' +  ','.join(vs) + ')')

    stmts = values_batch(table, vals)
    exe_many(stmts)

def insert_tip():
    table = 'tip'
    attrs = get_attrs('attrs/filtered/{}.txt'.format(table))
    vals = []
    with open(yelp_root + '/{}.json'.format(table)) as f:
        for i, l in enumerate(f):
            if i % 50000 == 0:
                print('read {} {}'.format(table, i))
            if i != 0 and i % 100000 == 0:
                stmts = values_batch(table, vals)
                exe_many(stmts)
                vals = []

            j = json.loads(l)
            vs = [a[1] + get_val(j, a[0], '') + a[2] for a in attrs]
            vals.append('(' +  ','.join(vs) + ')')

    stmts = values_batch(table, vals)
    exe_many(stmts)


if __name__ == '__main__':
    # create_tables()
    # insert_user()
    # insert_business()
    # insert_review()
    insert_tip()
