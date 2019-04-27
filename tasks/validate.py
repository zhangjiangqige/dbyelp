import logging
import sys
from sklearn.feature_extraction import DictVectorizer

from db import dbutils
from tasks import parse_user_input
from tasks import D_tree, D_collecting_using_view


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
        'insert into business_train (select * from business limit 5000)',
        'insert into business_val (select * from business limit 5000 offset 5000)'
    ]
    for q in queries:
        dbutils.execute(q, print=True)


def split_review():
    queries = [
        'drop table if exists review_train;',
        'drop table if exists review_val;',
        'create table review_train like review;',
        'create table review_val like review;',
        'alter table review add index (business_id)',
        'insert into review_train (select * from review where business_id in (select business_id from business_train));',
        'insert into review_val (select * from review where business_id in (select business_id from business_val));'
    ]
    for q in queries:
        dbutils.execute(q, print=True)


# return average difference
def validate_decision_tree():
    if not D_tree.tree:
        return None

    L = D_collecting_using_view.split_params
    logger.info('validate using params: {}'.format(L))
    create_validation_view_sql = """\
        create view view_validation as
        (select B.business_id, U.user_id, B.stars, B.review_count, R.stars as review_stars, U.average_stars, U.fans, U.useful/U.review_count as useful_prop
        from business_val B
        join review_val R on B.business_id = R.business_id
        join user U on R.user_id = U.user_id);
    """

    drop_validation_view_sql = """\
        drop view view_validation;
    """

    with dbutils.connection.cursor() as cursor:
        cursor.execute(create_validation_view_sql)
        logger.info("create view successfully")
        cursor.execute("select * from view_validation")
        validation_list = cursor.fetchall()
        logger.info("collect successfully")
        cursor.execute(drop_validation_view_sql)
        answer_list = []
        for dic_i in validation_list:
            answer_list.append(dic_i["review_stars"])
            dic_i.pop("user_id")
            dic_i.pop("business_id")
            dic_i.pop("review_stars")
            dic_i["stars"] = str(dic_i["stars"])
            l_review_count = parse_user_input.parse_user_review_count(L)
            for index in range(len(l_review_count)-1):
                if int(dic_i['review_count']) > l_review_count[index] and int(dic_i['review_count']) <= l_review_count[index+1]:
                    dic_i['review_count'] = str(index)

            l_fans = parse_user_input.parse_user_fans(L)
            for index in range(len(l_fans)-1):
                if int(dic_i["fans"]) > l_fans[index] and int(dic_i["fans"]) <= l_fans[index+1]:
                    dic_i["fans"] = str(index)

            l_average_stars = parse_user_input.parse_user_average_stars(L)
            for index in range(len(l_average_stars)-1):
                if float(dic_i["average_stars"]) > l_average_stars[index] and float(dic_i["average_stars"]) <= l_average_stars[index+1]:
                    dic_i["average_stars"] = str(index)

            l_useful_prop = parse_user_input.parse_user_useful_prop(L)
            for index in range(len(l_useful_prop)-1):
                if float(dic_i["useful_prop"]) > l_useful_prop[index] and float(dic_i["useful_prop"]) <= l_useful_prop[index+1]:
                    dic_i["useful_prop"] = str(index)
        vec = DictVectorizer()
        dummy_x = vec.fit_transform(validation_list).toarray()
        # test_0 = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0,]
        # test = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,]
        # predict = D_tree.tree.predict(test)
        # print ('predict:', str(predict))
        total_error = 0
        count_bad = 0
        for i in range(len(dummy_x)):
            predict = D_tree.tree.predict(dummy_x[i])
            if predict == -1:
                count_bad = count_bad + 1
            else:
                total_error = total_error + abs(answer_list[i] - int(predict))
        average_error = total_error / (len(dummy_x)-count_bad)
        print("average error:", str(average_error))
    return average_error
