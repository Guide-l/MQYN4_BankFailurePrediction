pip install tpot

from tpot import TPOTClassifier
import pandas as pd
import csv

file_name = #TRAINING SET FILE PATH
train_data = pd.read_csv(file_name, header = 0)
file_name = #TESTING SET FILE PATH
test_data = pd.read_csv(file_name, header = 0)
#print(train_data,test_data)

header = list(train_data.columns)

x_train = train_data.iloc[:,0:-1].values
y_train = train_data.iloc[:,-1].values
x_test = test_data.iloc[:,0:-1].values
y_test = test_data.iloc[:,-1].values

tpot = TPOTClassifier(generations=5, population_size=50, cv=5,
                                    random_state=42, verbosity=2)
tpot.fit(x_train,y_train)

print(tpot.score(x_test,y_test))

tpot = TPOTClassifier(generations=5, population_size=50, cv=5,
                                    random_state=42, verbosity=2)
score = []
for i in header:
  print(i)
  x_train = train_data[i].values
  x_train = x_train.reshape(x_train.shape[0],1)
  y_train = train_data.iloc[:,-1].values
  x_test = test_data[i].values
  x_test = x_test.reshape(x_test.shape[0],1)
  y_test = test_data.iloc[:,-1].values
  tpot.fit(x_train,y_train)
  score.append(tpot.score(x_test,y_test))

with open('Fields_testing_delta.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerow(score)

