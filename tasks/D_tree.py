import math
import collections

def entropy(rows: list) -> float:

    result = collections.Counter()
    result.update(rows)
    rows_len = len(rows)
    assert rows_len   
    ent = 0.0
    for r in result.values():
        p = float(r) / rows_len
        ent -= p * math.log2(p)
    return ent


def condition_entropy(future_list: list, result_list: list) -> float:
    entropy_dict = collections.defaultdict(list)  
    for future, value in zip(future_list, result_list):
        entropy_dict[future].append(value)
    ent = 0.0
    future_len = len(future_list)
    for value in entropy_dict.values():
        p = len(value) / future_len * entropy(value)
        ent += p

    return ent


def gain(future_list: list, result_list: list) -> float:
    info = entropy(result_list)
    info_condition = condition_entropy(future_list, result_list)
    return info - info_condition

class DecisionNode(object):
    def __init__(self, col=-1, data_set=None, labels=None, results=None, tb=None, fb=None):
        self.has_calc_index = []    
        self.col = col              
        self.data_set = data_set    
        self.labels = labels        
        self.results = results      
        self.tb = tb                
        self.fb = fb                



def if_split_end(result_list: list) -> bool:
    result = collections.Counter()
    result.update(result_list)
    return len(result) == 1

def choose_best_future(data_set: list, labels: list, ignore_index: list) -> int:
    result_dict = {}  
    future_num = len(data_set[0])
    for i in range(future_num):
        if i in ignore_index:
            continue
        future_list = [x[i] for x in data_set]
        result_dict[i] = gain(future_list, labels) 
    ret = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return ret[0][0]


class DecisionTreeClass():
    def __init__(self):
        self.future_num = 0      
        self.tree_root = None    

    def build_tree(self, node: DecisionNode):
        if if_split_end(node.labels):
            node.results = node.labels[0] 
            return
        best_index = choose_best_future(node.data_set, node.labels, node.has_calc_index)
        node.col = best_index

        tb_index = [i for i, value in enumerate(node.data_set) if value[best_index]]
        tb_data_set     = [node.data_set[x] for x in tb_index]
        tb_data_labels  = [node.labels[x] for x in tb_index]
        tb_node = DecisionNode(data_set=tb_data_set, labels=tb_data_labels)
        tb_node.has_calc_index = list(node.has_calc_index)
        tb_node.has_calc_index.append(best_index)
        node.tb = tb_node

        fb_index = [i for i, value in enumerate(node.data_set) if not value[best_index]]
        fb_data_set = [node.data_set[x] for x in fb_index]
        fb_data_labels = [node.labels[x] for x in fb_index]
        fb_node = DecisionNode(data_set=fb_data_set, labels=fb_data_labels)
        fb_node.has_calc_index = list(node.has_calc_index)
        fb_node.has_calc_index.append(best_index)
        node.fb = fb_node

        if tb_index:
            self.build_tree(node.tb)
        if fb_index:
            self.build_tree(node.fb)

    def clear_tree_example_data(self, node: DecisionNode):
        del node.has_calc_index
        del node.labels
        del node.data_set
        if node.tb:
            self.clear_tree_example_data(node.tb)
        if node.fb:
            self.clear_tree_example_data(node.fb)

    def fit(self, x: list, y: list):
        self.future_num = len(x[0])
        self.tree_root = DecisionNode(data_set=x, labels=y)
        self.build_tree(self.tree_root)
        self.clear_tree_example_data(self.tree_root)

    def _predict(self, data_test: list, node: DecisionNode):
        if node.results:
            return node.results
        col = node.col
        if data_test[col]:
            return self._predict(data_test, node.tb)
        else:
            return self._predict(data_test, node.fb)

    def predict(self, data_test):
        """
        预测
        """
        return self._predict(data_test, self.tree_root)

def build(dummy_x, dummy_y):
    tree = DecisionTreeClass()
    tree.fit(dummy_x, dummy_y)






