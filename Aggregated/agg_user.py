#Required libraries for the program

import pandas as pd
import json
import os

from sqlalchemy import create_engine

root_folder = '/content/pulse/data/aggregated/user/country/india/state'  # Your main directory
all_data = []

# Recursively walk through all folders
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if filename.endswith('.json'):
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    all_data.append(data)  # Collect JSON data
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON file: {file_path}")

# Now all_data contains data from all valid JSON files
#print(all_data)
# To get selected data
agguser={'States':[], 'Yr':[],'Quater':[],'Registered_users':[], 'App_opens':[]}

# Corrected path for aggregated user state data
path="pulse/data/aggregated/user/country/india/state/"
Agg_state_list=os.listdir(path)

for state in Agg_state_list:
    p_s=os.path.join(path, state)
    if os.path.isdir(p_s):
        Agg_yr_list=os.listdir(p_s)
        for year in Agg_yr_list:
            p_y=os.path.join(p_s, year)
            if os.path.isdir(p_y) and year.isdigit():
                Agg_qtr_list=os.listdir(p_y)
                for qtr in Agg_qtr_list:
                    p_q=os.path.join(p_y, qtr)
                    if os.path.isfile(p_q):
                        Data=open(p_q,'r')
                        D=json.load(Data)
                        # Extract data from 'aggregated' and 'usersByDevice'
                        if 'aggregated' in D['data']:
                            agguser['Registered_users'].append(D['data']['aggregated']['registeredUsers'])
                            if 'appOpens' in D['data']['aggregated']:
                                agguser['App_opens'].append(D['data']['aggregated']['appOpens'])
                            else:
                                agguser['App_opens'].append(None) # Handle cases where 'appOpens' might be missing
                            agguser['States'].append(state)
                            agguser['Yr'].append(year)
                            agguser['Quater'].append(int(qtr.strip('.json')))

#Succesfully created a dataframe
Agg_User=pd.DataFrame(agguser)
print(Agg_User.head(5))
#<------------------------------------------------------------------------------------------->
Agg_User = pd.DataFrame(agguser)

# Create database engine
engine = create_engine("postgresql+psycopg2://sugeetha_user:1sZvre5q7iok697JpIre1qCJiu5qJ9AV@dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com/sugeetha")

# Write DataFrame to SQL table
Agg_User.to_sql('agguser', con=engine, if_exists='replace', index=False)
