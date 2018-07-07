import pandas as pd
import numpy as np
import logging
from collections import Counter
glossary_dict = {}
initial_keyword_val = 1
ignore_city = ["NOIDA", "NOID", "UTTER PRADESH", "NEW DELHI", "DELHI", "UTTAR PRADESH", "GAUTAM BUDH N", "GAUTAM BUDH", "MEERUT", "GURGAON", "IN", "NOID"]

expensedata = pd.read_csv("expense.csv")

# Data Cleaning
expensedata["Merchant"] = expensedata["Merchant"].map(lambda x: x.replace(".", " ").strip())

# Training DataSet
expensedata_train = expensedata.drop_duplicates('Merchant')
expensedata_train = expensedata_train.loc[expensedata_train['Y'].notnull()]
expensedata_train = pd.DataFrame(expensedata_train)
labelslist = list(set(expensedata_train['Y'].values))

# Data Mining
expensedata_train_np = np.array(expensedata_train)
for i in range(len(expensedata_train_np)):
    for keyword in expensedata_train_np[i][1].split():
        keyword = keyword.upper()
        if keyword in ignore_city:
            continue
        if keyword not in glossary_dict:
            glossary_dict[keyword] = [expensedata_train_np[i][5]]
        else:
            glossary_dict[keyword].append(expensedata_train_np[i][5])
for key, values in glossary_dict.items():
    glossary_dict[key] = dict(Counter(values))
    #print(key, glossary_dict[key])

expensedata_testindexes = np.where(expensedata['Y_'].isnull())
print(expensedata_testindexes)

for i in expensedata_testindexes:
    expensedata.loc[i,'Y_'] ="HELLO"
print(expensedata)
#
# for merchant in expensedata_test['Merchant'].values:
#     merchant = merchant.upper()
#     keylist = []
#     for keyword in merchant.split():
#         if keyword in glossary_dict:
#             keylist += glossary_dict[keyword]
#     #y_[i] = max(keylist,key=keylist.count)
#     expensedata_test['Y_'][i] = max(keylist,key=keylist.count)
#
#     i += 1
#     # print(keylist, merchant)
#     # print(max(keylist,key=keylist.count))
#     # exit(0)
# #expensedata_test['Y_'] = y_
# print(expensedata_test)