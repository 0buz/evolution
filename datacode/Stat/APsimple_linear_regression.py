import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#==========================  Data Preprocessing   ======================================================================
# Importing the dataset
dataset = pd.read_csv('Salary_Data.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1/3, random_state=0)

# print("\nX train", X_train)
# print("\nX test", X_test)
# print("\ny train", y_train)
# print("\ny test", y_test)

# Feature Scaling
# from sklearn.preprocessing import StandardScaler
#
# sc_X = StandardScaler()     #create instance object of scaler
# X_train = sc_X.fit_transform(X_train)
# X_test = sc_X.transform(X_test)

# sc_y = StandardScaler()
# y_train = sc_y.fit_transform(y_train)

#=======================================================================================================================


# Fitting Simple Linear Regression to the Training set
from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
regressor.fit(X_train, y_train)
# here above, the simple linear regressor learnt the correlation between no. of years of experience on the training set;
# the model will be applied to the Test set next, to predict new observations

# Predicting the Test set results
# we will create a vector of predicted salaries:
y_pred = regressor.predict(X_test)   # y_pred are the salaries predicted, y_test are the real salaries


# Visualising the Training set results (real observations)
plt.scatter(X_train,y_train, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')    # we want the predicted salaries of the TRAINING set
plt.title('Salary vs Experience (Training Set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()


# Visualising the Test set results
plt.scatter(X_test, y_test, color='red')
plt.plot(X_train, regressor.predict(X_train), color='blue')    # no need to change this as the results will be the same; our regressor is already trained on the training set
plt.title('Salary vs Experience (Test Set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()