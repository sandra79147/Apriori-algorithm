import pandas as pd
import random

class SupportException(Exception):
    def __init__(self, wartosc):
        self.wartosc = wartosc
    def __str__(self):
        return self.wartosc

class Apriori:

    support_dict = {}
    removed_sets = []

    def __init__(self,data,min_support, min_confidence, min_lift, min_length):
        self.transactions = data
        self.transactions_number = len(data)
        self.items = list(data.columns)
        self.min_support = min_support
        self.min_confidence = min_confidence

    def fit(self):
        #create support of 1-item sets
        all_support = {}
        for item in self.items:
            try:
                self.support_dict[item] = self.support(item)
            except SupportException:
                pass
        last = self.support_dict
        all_support[1] = self.support_dict
        for k in range(len(self.items) - 1):
            support = self.k_item_support(last,k + 2)
            if bool(support) is True:
                all_support[k + 2] = support
            else:
                break
            last = support
        print(all_support)
        print("\n \n")
        conf = self.confidence(all_support, k)
        print(conf)

    def support(self,item):
        support = sum(self.transactions[item]) / self.transactions_number
        if support >= self.min_support:
            return support

    def k_item_support(self,last_set_item, k):
        ksupport_dict ={}
        for key in last_set_item.keys():
            last_list = []
            if type(key) is tuple:
                last_list = list(key)
            else:
                last_list.append(key)
            for item in self.items:
                last_list.append(item)
                set_item = tuple(set(last_list))
                count = 0
                if set_item not in ksupport_dict.keys() and len(set_item) == k:
                    count = self.counting_transactions(self.transactions, set_item)
                    support = count / self.transactions_number
                    if support >= self.min_support:
                        ksupport_dict[set_item] = count / self.transactions_number
                last_list.remove(item)
        return ksupport_dict

    def counting_transactions(self,df, set_item):
        for el in set_item:
            condition = df[el] == 1
            df = df[condition]
        return len(df)
    
    def confidence(self,ksupport_dict, k):
        confidence_values = {}
        last_set = ksupport_dict[k + 1]
        for set_items in last_set.keys():
            size_subsets = k
            confidence_values[set_items] = {}
            while size_subsets>0:
                for el in ksupport_dict[k].keys():
                    if set(el).issubset(set(set_items)) or el in set(set_items):
                        confidence = last_set[set_items] / ksupport_dict[k][el]
                        confidence_values[set_items][el] = confidence
                size_subsets = size_subsets - 1 
        return confidence_values

            







#TEST
data = []
for i in range(7):
    data.append(random.sample([0]*2 + [1]*4, 6))

print(data)
# Create the pandas DataFrame 
df = pd.DataFrame(data, columns = ["Paper", "Pen", "Pencil", "Chalk" , "Crayons" , "Eraser"]) 
print(df)


A = Apriori(df,min_support = 0.5, min_confidence = 0.5, min_lift = 0.1, min_length = 2)
A.fit()
