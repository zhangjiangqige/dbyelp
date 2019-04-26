import sys
import csv
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn import tree
import D_tree

sys.path.append("../db")

import dbutils


create_training_sub_sql = """\
create table training_sub(
select * from (select business_id, stars, review_count from business) as B
natural join
(select user_id, business_id, stars as review_stars from review) as C
);
"""

create_training_sql = """\
create table training(
select * from training_sub natural join 
(select user_id, average_stars, fans, useful/review_count as useful_prop from user) as U
);
"""

update_review_count_1_sql = """\
update training set review_count = 1 where review_count < 50;
"""

update_review_count_2_sql = """\
update training set review_count = 2 where review_count >=50 and review_count < 100;
"""

update_review_count_3_sql = """\
update training set review_count = 3 where review_count >=100;
"""

update_fans_1_sql = """\
update training set fans = 1 where fans < 1000;
"""

update_fans_2_sql = """\
update training set fans = 2 where fans >= 1000 and fans < 2000;
"""

update_fans_3_sql = """\
update training set fans = 3 where fans >= 2000;
"""

update_useful_prop_1_sql = """\
update training set useful_prop = 1 where useful_prop <10;
"""

update_useful_prop_2_sql = """\
update training set useful_prop = 2 where useful_prop >= 10 and useful_prop < 15;
"""

update_useful_prop_3_sql = """\
update training set useful_prop = 3 where useful_prop >=15;
"""
update_average_stars_0.5_sql = """\
update training set average_stars = 0.5 where average_stars > 0 and average_stars <= 1;
"""

update_average_stars_1.5_sql = """\
update training set average_stars = 1.5 where average_stars > 1 and average_stars <= 2;
"""

update_average_stars_2.5_sql = """\
update training set average_stars = 2.5 where average_stars > 2 and average_stars <= 3;
"""

update_average_stars_3.5_sql = """\
update training set average_stars = 3.5 where average_stars > 3 and average_stars <= 4;
"""

update_average_stars_4.5_sql = """\
update training set average_stars = 4.5 where average_stars > 4 and average_stars <= 5;
"""

drop_training1_sql = """\
drop table training1;
"""

drop_training_sql = """\
drop table training;
"""

def collecting():
    dbutils.connect_db ("marmoset04.shoshin.uwaterloo.ca", "j892zhan", "12345678", "db356_j892zhan")

    with dbutils.connection.cursor() as cursor:
        cursor.execute(create_training_sub_sql)
        print("create traing_sub table successfully")
        cursor.execute(create_training_sql)
        print("create training table successfully")
        cursor.execute(update_review_count_1_sql)
        cursor.execute(update_review_count_2_sql)
        cursor.execute(update_review_count_3_sql)
        print("update review_count column successfully")
        cursor.execute(update_fans_1_sql)
        cursor.execute(update_fans_2_sql)
        cursor.execute(update_fans_3_sql)
        print("update fans column successfully")
        cursor.execute(update_useful_prop_1_sql)
        cursor.execute(update_useful_prop_2_sql)
        cursor.execute(update_useful_prop_3_sql)
        print("update useful_prop column successfully")
        cursor.execute(update_average_stars_0.5_sql)
        cursor.execute(update_average_stars_1.5_sql)
        cursor.execute(update_average_stars_2.5_sql)
        cursor.execute(update_average_stars_3.5_sql)
        cursor.execute(update_average_stars_4.5_sql)
        print("update average stars column successfully")

        
def training():
    with dbutils.connection.cursor() as cursor:
        cursor.execute("select count(*) as number from training")
        result_num = cursor.fetchall()
        num = result_num[0]["number"]
        print (num)
        i = 0
        future_list = []
        while(i < num):
            cursor.execute("select * from training limit 100000 offset %s",i)
            fetch_list = cursor.fetchall()
            future_list = future_list + fetch_list
            i = i + 100000
        print ("collect successfully")

        cursor.execute(drop_training1_sql)
        cursor.execute(drop_training1_sql)
        print("drop table successfully")

    answer_list = []
    for dic_i in future_list:    
        answer_list.append(str(dic_i["review_stars"]))
        dic_i.pop("user_id")
        dic_i.pop("business_id")
        dic_i.pop("review_stars")
        dic_i["stars"] = str(dic_i["stars"])
        dic_i["review_count"] = str(dic_i["review_count"])
        dic_i["average_stars"] = str(dic_i["average_stars"])
        dic_i["fans"] = str(dic_i["fans"])
        dic_i["useful_prop"] = str(int(dic_i["useful_prop"]))

    vec = DictVectorizer()
    dummy_x = vec.fit_transform(future_list).toarray()

    lb = preprocessing.LabelBinarizer()
    dummy_y = lb.fit_transform(answer_list)

    clf = tree.DecisionTreeClassifier(criterion='entropy')
    clf.fit(dummy_x, dummy_y)
    print("build successfully")

def testing(test_x):
    predict = clf.predict([test_x])
    print("predict:", predict)

    
    


    


