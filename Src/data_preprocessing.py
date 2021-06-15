import numpy as np
import pandas as pd
import random
import csv

file_name = #DATASET FILE PATH
data = pd.read_csv(file_name, header= 0)
print(data)
header = list(data.columns)

#replace N/A with 0.0
#replace Y and N with 1 and 0 
data_array = data.to_numpy()
records_no = len(data_array)
for x in range (records_no):
  for y in range (len(data_array[x])):
    if (data_array[x][y] == 'Y'):
      data_array[x][y] = 1
    elif (data_array[x][y] == 'N'):
      data_array[x][y] = 0
data_array = data_array.astype('float64')
data_array = np.nan_to_num(data_array)
print(data_array)

def write_file(header, data, file_name):
  with open('/content/drive/MyDrive/newData/'+file_name+'.csv', 'w', encoding='UTF8', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(header)
      writer.writerows(data)

def get_delta_data(header, data):
  delta_data_list = []
  delta_header = []

  for record in data:
    temp_list = []
    for fields in range(0,len(record)-1,2):
      val = record[fields+1]/record[fields]
      if (np.isnan(val) or np.isinf(val)):
        temp_list.append(0.0)
      else:
        temp_list.append(val)

    temp_list.append(record[-1])
    delta_data_list.append(temp_list)
  for i in range (0, len(header)-1, 2 ):
    #delta_header.append('delta_'+ header[i+1])
    delta_header.append('delta_'+ header[i+1][5:])
  delta_header.append(header[-1])

  return delta_header, delta_data_list

del_header, del_data = get_delta_data(header, data_array)

write_file(del_header, del_data, #FILENAME)
