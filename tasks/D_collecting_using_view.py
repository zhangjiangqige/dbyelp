import sys
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn import tree

from db import dbutils
from tasks import D_tree
from dbyelp import init
from tasks import parse_user_input

create_training_view_sql= """\
create view view_training as 
(select B.business_id, U.user_id, B.stars, B.review_count, R.stars as review_stars, U.average_stars, U.fans, U.useful/U.review_count as useful_prop
    from business_train B
    join review_train R on B.business_id = R.business_id
    join user U on R.user_id = U.user_id);
"""

drop_training_view_sql = """\
drop view view_training;
"""

def building():
    init()
    L = {'review_count': [0,50,100,9000], 'fans':[0,1000,2000,3000],'average_stars':[0,0.5,1.5,2.5,3.5,4.5,5],'useful_prop':[0,10,15,500]}
    with dbutils.connection.cursor() as cursor:
        cursor.execute(create_training_view_sql)
        print("create view successfully")
        cursor.execute("select * from view_training")
        future_list = cursor.fetchall()
        print ("collect successfully")
        cursor.execute(drop_training_view_sql)
        answer_list = []
        for dic_i in future_list:
            answer_list.append(str(dic_i["review_stars"]))
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
    dummy_x = vec.fit_transform(future_list).toarray()    
    D_tree.build(dummy_x, answer_list)
    print("build successfully")

            
            
