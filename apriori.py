import pandas as pd

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
            all_support[k + 2] = support
            last = support
        print(all_support)

    def support(self,item):
        support = sum(self.transactions[item]) / self.transactions_number
        if support < self.min_support:
            raise SupportException('Item support value x is less than min_support: {}'.format(support))
        else:
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
                    for index, row in df.iterrows():
                        n = 0
                        for el in set_item:
                            if row[el] > 0 and n == len(set_item) - 1:
                                count = count + 1 
                                break
                            elif row[el] < 0:
                                break
                            n = n + 1
                    support = count / self.transactions_number
                    if support < self.min_support:
                        print('Support value is less than min_support: {} -\n {}'.format(support,set_item))
                    else:
                        ksupport_dict[set_item] = count / self.transactions_number
                last_list.remove(item)
        return ksupport_dict

    #def confidence():



    