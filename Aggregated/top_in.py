#Required libraries for the program

import pandas as pd
import json
import os

from sqlalchemy import create_engine

#This is to direct the path to get the data as states

path="pulse/data/top/insurance/country/india/state/" # Added the missing slash here
Top_insurance_state_list=os.listdir(path)
#Agg_state_list--> to get the list of states in India

#<------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------>#

#This is to extract the data's to create a dataframe

topin={'States':[], 'Yr':[],'Quater':[],'Entity_Name':[], 'Transacion_count':[], 'Transacion_amount':[], 'Entity_type':[]}

for state in Top_insurance_state_list:
    p_s=os.path.join(path, state)
    if os.path.isdir(p_s):
        year_list=os.listdir(p_s)
        for year in year_list:
            p_y=os.path.join(p_s, year)
            if os.path.isdir(p_y) and year.isdigit():
                qtr_list=os.listdir(p_y)
                for qtr_file in qtr_list:
                    p_q=os.path.join(p_y, qtr_file)
                    if os.path.isfile(p_q):
                        Data=open(p_q,'r')
                        D=json.load(Data)
                        # Check for 'states', 'districts', and 'pincodes' keys
                        for entity_type in ['states', 'districts', 'pincodes']:
                            if entity_type in D['data'] and D['data'][entity_type] is not None:
                                for entity_data in D['data'][entity_type]:
                                    Name=entity_data['entityName']
                                    count=entity_data['metric']['count']
                                    amount=entity_data['metric']['amount']
                                    topin['Entity_Name'].append(Name)
                                    topin['Transacion_count'].append(count)
                                    topin['Transacion_amount'].append(amount)
                                    topin['States'].append(state)
                                    topin['Yr'].append(year)
                                    topin['Quater'].append(int(qtr_file.strip('.json')))
                                    topin['Entity_type'].append(entity_type)

#Succesfully created a dataframe
Top_Insurance=pd.DataFrame(topin)
print(Top_Insurance)
#<------------------------------------------------------------------------------------------>
engine = create_engine("postgresql+psycopg2://sugeetha_user:1sZvre5q7iok697JpIre1qCJiu5qJ9AV@dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com/sugeetha")

# Write DataFrame to SQL table
Top_Insurance.to_sql('topinsurance', con=engine, if_exists='replace', index=False)
