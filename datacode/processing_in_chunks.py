import pandas as pd
import matplotlib.pyplot as plt

chunk_iter = pd.read_csv('datacode/datatest.csv',chunksize=20000)

memory_footprints=[]
for chunk in chunk_iter:
    used_mem=chunk.memory_usage(deep=True).sum()/(1024*1024)
    memory_footprints.append(used_mem)


plt.hist(memory_footprints)
plt.show()