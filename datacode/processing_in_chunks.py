import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#dtypes = {"posted_date": "datetime64[ns]", "created_date": "datetime64[ns]"}
chunk_iter = pd.read_csv('datacode/datatest.csv',chunksize=25000, parse_dates=['posted_date','created_date'])

memory_footprints=[]
age=[]

for chunk in chunk_iter:
    used_mem=chunk.memory_usage(deep=True).sum()/(1024*1024)
    memory_footprints.append(used_mem)
    cd=pd.Timestamp(chunk['created_date'][0], tzinfo='UTC')
    pd = pd.Timestamp(chunk['posted_date'][0], tzinfo='UTC')
    diff = (chunk['created_date'], chunk['posted_date'])
    diff=cd-pd
    age.append(diff)

#print(type(chunk['posted_date']))
print(age)
# lifespans_dist = pd.concat(age)
# print(lifespans_dist)
# ========================

# plt.hist(memory_footprints)
# plt.show()