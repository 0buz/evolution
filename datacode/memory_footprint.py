import pandas as pd
import numpy as np

df = pd.read_csv('datacode/datatest.csv')

print(df.info())  # memory usage of dataframe
print(df.size)  # number of elements in the dataframe
print(df.info(memory_usage="deep"))  # info with column type and true total memory footprint
print(df.memory_usage(deep=True))  # true memory usage ***per column***
print(df.select_dtypes(
    include=['object']).isnull().sum())  # count how many null values exist in each column of type 'object'

print(df[['posted_date', 'created_date']].memory_usage(deep=True).sum() / 1048576)

# ========  Calculate total memory usage for columns of type 'object'  =========================
obj_cols = df.select_dtypes(include=['object'])
obj_cols_mem = obj_cols.memory_usage(deep=True)
obj_cols_sum = obj_cols_mem.sum() / 1048576  # divide by 2^20 to get result in MB
print(f"DF columns of selected type use {obj_cols_sum} MB of memory")
# =============================================================================================


# ================ Check min and max values for each subtype ==================================
# checking for int in this example
int_types = ["int8", "int16", "int32", "int64"]
for it in int_types:
    print(np.iinfo(it))

# Or, get just value of interest
print(np.iinfo("int8").min)
print(np.iinfo("int8").max)
# =============================================================================================

# =========== Optimise memory usage for numeric columns by changing data type ==================
columns = ['id', 'owner_id']

# using .astype()
for col in columns:
    col_max = df[col].max()
    col_min = df[col].min()

    if col_max < np.iinfo("int8").max and col_min > np.iinfo("int8").min:
        df[col] = df[col].astype("int8")
    elif col_max < np.iinfo("int16").max and col_min > np.iinfo("int16").min:
        df[col] = df[col].astype("int16")
    elif col_max < np.iinfo("int32").max and col_min > np.iinfo("int32").min:
        df[col] = df[col].astype("int32")
    elif col_max < np.iinfo("int64").max and col_min > np.iinfo("int64").min:
        df[col] = df[col].astype("int64")
    print(df[col].dtype)
    print(df[col].memory_usage(deep=True))

# using pd.to_numeric() is the preferred option; Note: downcast='integer', not int
for col in columns:
     df[col] = pd.to_numeric(df[col], downcast='integer')
     print(df[col].dtype)
# =============================================================================================

#=============== Convert to datetime =========================================================
columns = ['posted_date', 'created_date']
for col in columns:
     df[col] = pd.to_datetime(df[col], utc=True)
     print(df[col].dtype)
print(df[['posted_date', 'created_date']].memory_usage(deep=True))
print(f"Total memory usage for these columns: {df[['posted_date', 'created_date']].memory_usage(deep=True).sum() / 1048576:.4f} MB")
# =============================================================================================

#=============== Convert to type category =======================================================
df['type'] = df['type'].astype('category')
print(df['type'].memory_usage(deep=True))
print(f"Total memory usage for these columns: {df['type'].memory_usage(deep=True) / 1048576:.4f} MB")

print("These are the category codes:", df['type'].cat.categories)

columns = ['type', 'recruiter']
for col in columns:
     df[col] = df[col].astype('category')
print(f"Total memory usage for these columns: {df[columns].memory_usage(deep=True).sum() / 1048576:.4f} MB")

# =============================================================================================

obj_cols = df.select_dtypes(include=['object'])
for col in obj_cols.columns:
     num_unique_values = len(df[col].unique())
     #duplicates=moma[col].duplicated(keep=False).sum()
     num_total_values = len(df[col])
     print(f"For column {col} there are {num_unique_values} unique values out of {num_total_values} values.")
     if num_unique_values / num_total_values < 0.5:
          df[col] = df[col].astype('category')

print(df.info(memory_usage='deep'))
# =============================================================================================


#======= Read csv with optimal column types =====================================
dtypes = {"ConstituentBeginDate": "float", "ConstituentEndDate": "float"}
chunk_iter = pd.read_csv("moma.csv", chunksize=250, dtype=dtypes)
lifespans = []
for chunk in chunk_iter:
    diff = chunk['ConstituentEndDate'] - chunk['ConstituentBeginDate']
    lifespans.append(diff)
lifespans_dist = pd.concat(lifespans)
print(lifespans_dist)
# =============================================================================================