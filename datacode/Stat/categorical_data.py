# Data Preprocessing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datacode import settings

# Importing the dataset
dataset = pd.read_csv(settings.CSVFILE)

X = dataset.iloc[:, :-1].values  # matrix of features (all rows, all columns except last column)
y = dataset.iloc[:, 3].values  # vector of observations  (all rows, and column on index 3)

# Taking care of missing data
from sklearn.impute import SimpleImputer

imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
imputer = imputer.fit(X[:, 1:3])   #define the scope for impute
X[:, 1:3] = imputer.transform(X[:, 1:3])    #impute - replace all "NaN" with the mean value in that column


# Encoding categorical data
# Encoding the Independent Variable
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer



ct = ColumnTransformer([('encoder', OneHotEncoder(), [0])], remainder='passthrough')
X = np.array(ct.fit_transform(X), dtype=np.float)

# labelencoder_X = LabelEncoder()     #instance of LableEncoder(), LableEncoder >>> Encode labels with value between 0 and n_classes-1
# X[:, 0] = labelencoder_X.fit_transform(X[:, 0])    #encodes Countries
print(X)
# onehotencoder = OneHotEncoder(categorical_features=[0])
# X = onehotencoder.fit_transform(X).toarray()     # e.g France = [1,0,0], Spain = [0,0,1] etc
# print("\n", X)

# Encoding the Dependent Variable
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)     #encodes Purchased

