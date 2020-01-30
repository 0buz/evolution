import pandas as pd
import numpy as np

moma = pd.read_csv('datacode/datatest.csv')

print(moma.info())  # memory usage of dataframe
print(moma.size)  # number of elements in the dataframe
print(moma.info(memory_usage="deep"))  # info with column type and true total memory footprint
print(moma.memory_usage(deep=True))  # true memory usage per dataframe column
print(moma.select_dtypes(
    include=['object']).isnull().sum())  # count how many null values exist in each column of type 'object'

print(moma[['posted_date', 'created_date']].memory_usage(deep=True).sum()/1048576)

# ========  Calculate total memory usage for columns of type 'object'  =========================
obj_cols = moma.select_dtypes(include=['object'])
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
    col_max = moma[col].max()
    col_min = moma[col].min()

    if col_max < np.iinfo("int8").max and col_min > np.iinfo("int8").min:
        moma[col] = moma[col].astype("int8")
    elif col_max < np.iinfo("int16").max and col_min > np.iinfo("int16").min:
        moma[col] = moma[col].astype("int16")
    elif col_max < np.iinfo("int32").max and col_min > np.iinfo("int32").min:
        moma[col] = moma[col].astype("int32")
    elif col_max < np.iinfo("int64").max and col_min > np.iinfo("int64").min:
        moma[col] = moma[col].astype("int64")
    print(moma[col].dtype)
    print(moma[col].memory_usage(deep=True))

# using pd.to_numeric() is the preferred option; Note: downcast='integer', not int
for col in columns:
     moma[col] = pd.to_numeric(moma[col], downcast='integer')
     print(moma[col].dtype)
# =============================================================================================

#=============== Convert to datetime =========================================================
columns = ['posted_date', 'created_date']
for col in columns:
     moma[col] = pd.to_datetime(moma[col],utc=True)
     print(moma[col].dtype)
print(moma[['posted_date', 'created_date']].memory_usage(deep=True))
print(f"Total memory usage for these columns: {moma[['posted_date', 'created_date']].memory_usage(deep=True).sum()/1048576:.4f} MB")
# =============================================================================================

#=============== Convert to type category =======================================================
moma['type'] = moma['type'].astype('category')
print(moma['type'].memory_usage(deep=True))
print(f"Total memory usage for these columns: {moma['type'].memory_usage(deep=True)/1048576:.4f} MB")

print("These are the category codes:",moma['type'].cat.categories)

columns = ['type', 'recruiter']
for col in columns:
     moma[col] = moma[col].astype('category')
print(f"Total memory usage for these columns: {moma[columns].memory_usage(deep=True).sum()/1048576:.4f} MB")

# =============================================================================================

obj_cols = moma.select_dtypes(include=['object'])
for col in obj_cols.columns:
     num_unique_values = len(moma[col].unique())
     #duplicates=moma[col].duplicated(keep=False).sum()
     num_total_values = len(moma[col])
     print(f"For column {col} there are {num_unique_values} unique values out of {num_total_values} values.")
     if num_unique_values / num_total_values < 0.5:
          moma[col] = moma[col].astype('category')

print(moma.info(memory_usage='deep'))



#======= Read csv with optimal column types =====================================
