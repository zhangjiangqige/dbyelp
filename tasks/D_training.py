import csv
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from sklearn import tree
import D_tree

data_file = open("ylep.csv", "r")
reader = csv.reader(data_file)
headers = next(reader)

future_list = []
label_list = []

for row in reader:
    label_list.append(row[-1])
    row_dict = {}
    for i in range(1, len(row) -1):
        row_dict[ headers[i] ] = row[i]
    future_list.append(row_dict)
data_file.close()
print(future_list)
print(label_list)

vec = DictVectorizer()
dummy_x = vec.fit_transform(future_list).toarray()

lb = preprocessing.LabelBinarizer()
dummy_y = lb.fit_transform(label_list)

print(dummy_x)
print(dummy_y)


clf = tree.DecisionTreeClassifier(criterion='entropy')
clf.fit(dummy_x, dummy_y)
print ("build successfully")

first_row = dummy_x[0, :]
new_row = list(first_row)
new_row[0] = 1
new_row[2] = 0

predict = clf.predict([new_row])

print("predict:", predict)