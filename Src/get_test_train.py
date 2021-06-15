import pandas as pd
import numpy as np
import csv 
import random

def write_file(header, data, file_name):
  with open('/content/drive/MyDrive/newData/'+file_name+'.csv', 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      writer.writerows(data)

def get_test_train_set(data, prop):
  #randomly select testing and training set
  records_no = len(data)
  test_data = []
  train_data = []

  test_prop = int(records_no * prop)
  temp_all = list(range(int(records_no/2)))

  temp_test = []
  for i in range (int(test_prop/2)):
    r = random.randint(0,len(temp_all)-1)
    temp_test.append(temp_all.pop(r))

  for i in temp_test:
    test_data.append(data[i])
    test_data.append(data[i + 581])

  for i in temp_all:
    train_data.append(data[i])
    train_data.append(data[i + 581])
  
  return test_data, train_data

file_name = #FILE PATH 
data = pd.read_csv(file_name, header= 0)
header = list(data.columns)
data_array = data.to_numpy()
data_list = data_array.tolist()
print(len(data_list))

test,train = get_test_train_set(data_list,0.2)
write_file(header, test, #FILE NAME)
write_file(header, train, #FILE NAME)

