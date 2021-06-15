import pandas as pd
import numpy as np
from datetime import datetime 
import requests
import csv
import random


def add_row (list_l, list_o,id_index, fail):
    #Processed 2 different yesrs of data into a single row data
    temp_list_l = list_l.split(",")
    temp_list_o = list_o.split(",")
    temp_list_l.pop(id_index)
    temp_list_o.pop(id_index)

    row_data =[]
    for i in range(len(temp_list_l)):
        if (temp_list_o[i] != ''):
            row_data.append(float(temp_list_o[i]))
        else:
            row_data.append('N/A')
        if (temp_list_l[i] != ''):
            row_data.append(float(temp_list_l[i]))
        else:
            row_data.append('N/A')
    if (fail):
        row_data.append('Y')
    else:
        row_data.append('N')
    return row_data


input_file = "/Users/kittilimjumroonrat/Desktop/Finalproject/Src/Data/failed_banks.csv"
failed_bank = pd.read_csv(input_file,header = 0)

fail_bank_cert_list = failed_bank['CERT'].tolist()
#MM/DD/YYYY
fail_date_list = failed_bank['FAILDATE'].tolist()


fields_list = ["NUMEMP","ASSET","CHBAL","CHBALI","SC","FREPO","LNLSNET","LNATRES","TRADE","bkprem","ore","intan","idoa",
          "liabeq","liab","dep","depi","depdom","iddepinr","frepp","tradel","idobrmtg","subnd","idoliab","eqtot",
          "eq","eqpp","eqcs","eqsur","equptot","eqconsub","nclnls","NCGTYPAR","oaienc","ernast","asstlt","asset5",
          "asset2","RWAJT","AVASSETJ", "OALIFINS", "OALIFGEN","OALIFSEP", "Oalifhyb","voliab","lnexamt","othbfhlb"
          "lnlssale","ucln","RBCT1J","RBCT2","uc","obsdir","instcnt","intinc","eintexp","nim","elnatr","nonii",
          "ifiduc","iserchg","igltrad","idothnii","nonix","esal","epremagg","IDEOTH","idpretx","iglsec","itax",
          "ibefxtr","extra","NETINBM","NETIMIN","netinc","ntlnls","eqcdiv","eqcstkrx","noij",
          "intincy","intexpy","nimy","noniiay","nonixay","ELNATRY","noijy","roa","roaptx","roe","roeinjr","ntlnlsr",
          "elnantr","iderncvr","eeffr","astempm","iddivnir","ERNASTR","lnatresr","lnresncr","nperfv","nclnlsr",
          "LNLSNTV","lnlsdepr","idlncorr","DEPDASTR","eqv","rbc1aaj","CBLRIND","IDT1CER","IDT1RWAJR","rbcrwaj"]

seperator = "%2C"
fields_str = seperator.join(fields_list).upper()

processed_data = []
header = []
out_of_time_data = []

for index in range (len(fail_bank_cert_list)):
    #FDIC certification number for each bank (unique ID)
    bank_cert = fail_bank_cert_list[index]
    
    #check fail date to obtain the correct report format
    fail_date = datetime.strptime(fail_date_list[index], '%m/%d/%Y').date()
    
    if (fail_date > datetime.strptime('01/01/2004', '%m/%d/%Y').date()):
        records_limit = 13
        two_yp = 9
    elif (fail_date > datetime.strptime('07/01/2003', '%m/%d/%Y').date()):
        records_limit = 12
        two_yp = 8
    elif (fail_date > datetime.strptime('01/01/2003', '%m/%d/%Y').date()):
        records_limit = 11
        two_yp = 7
    elif (fail_date > datetime.strptime('10/01/2002', '%m/%d/%Y').date()):
        records_limit = 10
        two_yp = 6
    elif (fail_date > datetime.strptime('07/01/2002', '%m/%d/%Y').date()):
        records_limit = 9
        two_yp = 6
    elif (fail_date > datetime.strptime('01/01/2002', '%m/%d/%Y').date()):
        records_limit = 8
        two_yp = 5
    elif (fail_date > datetime.strptime('10/01/2001', '%m/%d/%Y').date()):
        records_limit = 7
        two_yp = 5
    elif (fail_date > datetime.strptime('07/01/2001', '%m/%d/%Y').date()):
        records_limit = 6
        two_yp = 4
    elif (fail_date > datetime.strptime('01/01/2000', '%m/%d/%Y').date()):
        records_limit = 5
        two_yp = 4
    else:
        records_limit = 4
        two_yp = 3
        
    #Retrieve using API    
    retrieval_str = "https://banks.data.fdic.gov/api/financials?filters=CERT%3A"+str(bank_cert)+"&fields="+fields_str+"&sort_by=CALLYM&sort_order=DESC&limit="+str(records_limit)+"&format=csv&download=false"
    response = requests.get(retrieval_str)
    response_list = response.text.split("\n")

    #Seperate header
    header = response_list[0].split("\",\"")
    header[0] = header[0][1:]
    header[-1] = header[-1][:-1]
    id_index = header.index("ID")
    header.append("FAIL?")
    header.pop(id_index)

    processed_data.append(add_row(response_list[1], response_list[two_yp], id_index, True))
    out_of_time_data.append(add_row(response_list[4], response_list[-1], id_index, True))

    print(index)



input_file = "/Users/kittilimjumroonrat/Desktop/Finalproject/Src/Data/active_banks_new.csv"
active_bank = pd.read_csv(input_file,header = 0)

all_active_bank_cert_list = active_bank['CERT'].tolist()

active_bank_cert_list = []
for i in range (len(processed_data)):
    r = random.randint(0,len(active_bank_cert_list))
    active_bank_cert_list.append(all_active_bank_cert_list.pop(r))

records_limit = 13
    
for index in range (len(active_bank_cert_list)):
    
    #Retrieve using API    
    retrieval_str = "https://banks.data.fdic.gov/api/financials?filters=CERT%3A"+str(active_bank_cert_list[index])+"&fields="+fields_str+"&sort_by=CALLYM&sort_order=DESC&limit="+str(records_limit)+"&format=csv&download=false"
    response = requests.get(retrieval_str)
    response_list = response.text.split("\n")
    
    #Seperate header
    header = response_list[0].split("\",\"")
    header[0] = header[0][1:]
    header[-1] = header[-1][:-1]
    id_index = header.index("ID")
    header.append("FAIL?")
    header.pop(id_index)
    
    count = index + 581
    processed_data.append(add_row(response_list[1], response_list[-5], id_index, False))
    out_of_time_data.append(add_row(response_list[4], response_list[-1], id_index, False))
    
    print(count)


header_new = []
for i in header:
    header_new.append("(2YP)"+i)
    header_new.append(i)
header_new.pop(-2)
header_new_oot = []
for i in header:
    header_new_oot.append("(3YP)"+i)
    header_new_oot.append("(1YP)"+i)
header_new_oot.pop(-1)
header_new_oot.pop(-1)
header_new_oot.append('FAIL?')

#print(header)
#print(len(header))
#print(processed_data[0])
#print(len(processed_data[0]))
#print(processed_data[-1])
#print(len(processed_data[-1]))


with open('/Users/kittilimjumroonrat/Desktop/Finalproject/Src/Data/bank_dataset.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header_new)
    writer.writerows(processed_data)

with open('/Users/kittilimjumroonrat/Desktop/Finalproject/Src/Data/OOT_bank_dataset.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header_new_oot)
    writer.writerows(out_of_time_data)




