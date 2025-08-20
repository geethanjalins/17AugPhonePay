#Once created the clone of GIT-HUB repository then,
#Required libraries for the program

import pandas as pd
import json
import os

#This is to direct the path to get the data as states

path="pulse/data/aggregated/insurance/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

aggin={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}

for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              aggin['Transacion_type'].append(Name)
              aggin['Transacion_count'].append(count)
              aggin['Transacion_amount'].append(amount)
              aggin['State'].append(i)
              aggin['Year'].append(j)
              aggin['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Insurance=pd.DataFrame(aggin)
print(Agg_Insurance.tail(5))
