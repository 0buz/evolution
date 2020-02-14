import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pd.unique()
#==========================  Data Preprocessing   ======================================================================
# Importing the dataset
#dataset = pd.read_csv('./50_Startups.csv')
dataset = pd.read_csv(r"/home/adrian/Python/Machine Learning A-Z/Part 2 - Regression/Section 5 - Multiple Linear Regression/50_Startups.csv")
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 4].values

#Encoding categorical data
#Encoding the Independent Variable
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

ct = ColumnTransformer([('encoder', OneHotEncoder(), [3])], remainder='passthrough')     # encoding catagorical data (States) to Dummy Variables
X = np.array(ct.fit_transform(X), dtype=np.float)    # fitting to X

# Avoiding the Dummy Variable Trap
# the python lib for linear regression takes care of this automatically, so normaly we shouldn't need to do this
X = X[:,1:]    # get all rows, and all columns except the one with index 0

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
#=======================================================================================================================


# Fitting Multiple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
regressor.fit(X_train,y_train)

# Predicting the Test set results
y_pred = regressor.predict(X_test)


