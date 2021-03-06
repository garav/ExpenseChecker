import pandas as pd
import numpy as np
import logging
import os.path
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
            glossary_dict[keyword] = [expensedata_train_np[i][3]]
        else:
            glossary_dict[keyword].append(expensedata_train_np[i][3])
for key, values in glossary_dict.items():
    glossary_dict[key] = dict(Counter(values))
    # print(key, glossary_dict[key])

expensedata_testindexes = list(np.where(expensedata['Y_'].isnull())[0])
#print(expensedata_testindexes)

for i in expensedata_testindexes:

    for keyword in str(expensedata.loc[i,'Merchant']).split():
        keylist = []
        keyword = keyword.upper()
        if keyword in ignore_city:
            continue
        if keyword in glossary_dict:
            keylist += glossary_dict[keyword]

        if keylist:
            expensedata.loc[i, 'Y_'] = max(keylist, key=keylist.count)
        else:
            expensedata.loc[i, 'Y_'] = ""
    if os.path.exists("expense_copy.csv"):
        os.remove("expense_copy.csv")
    os.rename("expense.csv", "expense_copy.csv")

    expensedata.to_csv("expense.csv", index=False)

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