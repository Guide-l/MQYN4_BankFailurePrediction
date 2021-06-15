import pandas as pd 
import numpy as np

file_name = #TRAINING SET FILE PATH
train_data = pd.read_csv(file_name, header = 0)
file_name = #TESTING SET FILE PATH
test_data = pd.read_csv(file_name, header = 0)
print(train_data,test_data)

#Standardisation
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
train_data[train_data.columns] = sc.fit_transform(train_data[train_data.columns])
test_data[test_data.columns] = sc.fit_transform(test_data[test_data.columns])

x_train = train_data.iloc[:,0:-1].values
y_train = train_data.iloc[:,-1].values
x_test = test_data.iloc[:,0:-1].values
y_test = test_data.iloc[:,-1].values
print(x_train,y_train,x_test,y_test)

def test_accuracy(confusion_matrix):
  diagonal_sum = confusion_matrix.trace()
  sum = confusion_matrix.sum()
  return diagonal_sum / sum

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

kf = KFold(n_splits = 5, shuffle = True)
classifier = MLPClassifier()
cross_val_test_acc = []
for i in kf.split(train_data):
  classifier.fit(x_train,y_train)
  y_pred = classifier.predict(x_test)
  cm = confusion_matrix(y_pred, y_test)
  cross_val_test_acc.append(test_accuracy(cm))

print ("Accuracy of MLPClassifier : " + str(sum(cross_val_test_acc)/len(cross_val_test_acc) * 100) + "%")

>>> from sklearn.ensemble import RandomForestClassifier

kf = KFold(n_splits = 3, shuffle = True)
classifier = RandomForestClassifier()
#n_estimators=100, random_state=0
cross_val_test_acc = []
for i in kf.split(train_data):
  classifier.fit(x_train,y_train)
  y_pred = classifier.predict(x_test)
  cm = confusion_matrix(y_pred, y_test)
  cross_val_test_acc.append(test_accuracy(cm))

print ("Accuracy of RandomTreesClassifier : " + str(sum(cross_val_test_acc)/len(cross_val_test_acc) * 100) + "%")

from sklearn.svm import SVC

kf = KFold(n_splits = 5, shuffle = True)
classifier = SVC()
#gamma = 'auto'
cross_val_test_acc = []
for i in kf.split(train_data):
  classifier.fit(x_train,y_train)
  y_pred = classifier.predict(x_test)
  cm = confusion_matrix(y_pred, y_test)
  cross_val_test_acc.append(test_accuracy(cm))

print ("Accuracy of SVC : " + str(sum(cross_val_test_acc)/len(cross_val_test_acc) * 100) + "%")

