import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer


# Read in the data with `read_csv()'
data = pd.read_csv('CleanTwitteData.csv')

data = data.drop('Unnamed: 0', axis = 1)
#Delete row with dummy value
data = data.dropna(how='any',axis=0)

data['binary_class'] = data['sentiment']

X_train, X_test, y_train, y_test = train_test_split(data['Tweets'], data['binary_class'], random_state = 0)


#creating variable which assigns X_train to numbers
vect = CountVectorizer().fit(X_train)

X_train_vectorized = vect.transform(X_train)

#creating log regression

model = LogisticRegression()
model.fit(X_train_vectorized, y_train)

print(model.predict(vect.transform(['he is freaking awesome'])))