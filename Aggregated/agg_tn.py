#Required libraries for the program

import pandas as pd
import json
import os

from sqlalchemy import create_engine
#<-------------------------------------------------------------------------------------------->
#This is to direct the path to get the data as states

path="pulse/data/aggregated/transaction/country/india/state/"
Agg_state_list=os.listdir(path)
Agg_state_list
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

aggtn={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}

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
              aggtn['Transacion_type'].append(Name)
              aggtn['Transacion_count'].append(count)
              aggtn['Transacion_amount'].append(amount)
              aggtn['State'].append(i)
              aggtn['Year'].append(j)
              aggtn['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
Agg_Trans=pd.DataFrame(aggtn)

#<--------------------------------------------------------------------------------------------->
# Your DataFrame
Agg_Trans = pd.DataFrame(aggtn)

# Create database engine
engine = create_engine("postgresql+psycopg2://sugeetha_user:1sZvre5q7iok697JpIre1qCJiu5qJ9AV@dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com/sugeetha")

# Write DataFrame to SQL table
Agg_Trans.to_sql('aggtn', con=engine, if_exists='replace', index=False)

