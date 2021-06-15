import pandas as pd
import numpy as np
import csv

def write_file(filename,old_header,new_header,data,lenght):
  del_header_old = del_data.columns.tolist()
  with open('/content/drive/MyDrive/newData/'+filename+'.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(new_header)
    for i in range (lenght):
      list = []
      for j in new_header:
        list.append(data.iloc[i,old_header.index(j)])
      writer.writerow(list)

#Seperate ratio and general variables
file_name = #FILE PATH
del_data = pd.read_csv(file_name, header = 0)
del_header = del_data.columns.tolist()
print(del_data)

ratio_fields = ["intincy","nimy","noniiay","nonixay","ELNATRY","noijy","roa","roaptx","roe","roeinjr","ntlnlsr",
            "elnantr","eeffr","astempm","ERNASTR","lnatresr","lnresncr","nperfv","nclnlsr",
            "LNLSNTV","lnlsdepr","DEPDASTR","eqv","rbc1aaj","rbcrwaj"]
normal_fields = ["NUMEMP","ASSET","CHBAL","CHBALI","SC","FREPO","LNLSNET","LNATRES","TRADE","bkprem","ore","intan",
          "liabeq","liab","dep","depi","depdom","frepp","tradel","subnd","eqtot",
          "eq","eqpp","eqcs","eqsur","equptot","eqconsub","nclnls","NCGTYPAR","oaienc","ernast","asstlt","asset5",
          "asset2","RWAJT","AVASSETJ", "OALIFINS", "OALIFGEN","OALIFSEP", "Oalifhyb","voliab",
          "lnexamt","ucln","RBCT1J","RBCT2","uc","obsdir","intinc","eintexp","nim","elnatr","nonii",
          "ifiduc","iserchg","igltrad","nonix","esal","epremagg","iglsec","itax",
          "ibefxtr","extra","NETINBM","NETIMIN","netinc","ntlnls","eqcdiv","eqcstkrx","noij",]
for i in range (len(ratio_fields)):
  ratio_fields[i] = "delta_"+ratio_fields[i].upper()
ratio_fields.append('FAIL?')

for i in range (len(normal_fields)):
  normal_fields[i] = "delta_"+normal_fields[i].upper()
normal_fields.append('FAIL?')

#write to two seperate dataset files
write_file('test', del_data.columns.tolist(),ratio_fields, del_data, len(del_data))
write_file('test', del_data.columns.tolist(),normal_fields, del_data, len(del_data))

#Feature selection based on features score
file_name = #DATASET FILE PATH
data = pd.read_csv(file_name, header = 0)
header = data.columns.tolist()
print(data)
file_name = #FEATURE SCORE FILE PATH
fields_data = pd.read_csv(file_name, header = 0)

fields_data_list = []
fields_data_list.append(header)
fields_data_list.append(fields_data.iloc[0].tolist())

print(fields_data_list[0].index('FAIL?'))
test = fields_data_list[1][fields_data_list[0].index('delta_ROE')]

def get_fields_rank(data_list, order, lenght):
  list = data_list
  #Basic bubble sort
  n = len(list[0])
  for i in range(n-2):
      for j in range(0, n-i-1):
          if list[1][j] > list[1][j + 1] :
              list[0][j], list[0][j + 1] = list[0][j + 1], list[0][j]
              list[1][j], list[1][j + 1] = list[1][j + 1], list[1][j]
  if (order == 'D'):
    return list[0][len(list[0])-lenght-1:-1]
  else:
    return list[0][:lenght]

best = get_fields_rank(fields_data_list,'D',20)
worst = get_fields_rank(fields_data_list,'A',20)

print(best)
print(worst)

best.append('FAIL?')
 worst.append('FAIL?')

#Test validity
print(fields_data_list[1][fields_data_list[0].index('delta_ROE')] == test)

write_file('Best_OOT_20_set', data.columns.tolist(),best, data, len(data))
#write_file('Worst_20_set', data.columns.tolist(),worst, data, len(data))

#write to two seperate dataset files
write_file('Best_set', data.columns.tolist(),best, data, len(data))
write_file('Worst_set', data.columns.tolist(),worst, data, len(data))

all_fields = normal_fields[:-1] + ratio_fields[:-1]
print(len(all_fields))

a_counter = 0
i_counter = 0
r_counter = 0
for i in best:
  index = all_fields.index(i)
  if index < 47:
    a_counter = a_counter +1
  elif index < 69:
    i_counter = i_counter +1
  else:
    r_counter = r_counter +1
print(a_counter,i_counter,r_counter)

