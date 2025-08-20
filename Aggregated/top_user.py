#Required libraries for the program

import pandas as pd
import json
import os

from sqlalchemy import create_engine

root_folder = 'pulse/data/top/user/country/india/state'  # Your main directory
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

# To get selected data
topuser={'States':[],'Yr':[],'Quater':[],'Districts':[], 'Registered_users':[], 'Entity_type':[]}

# Corrected path for aggregated user state data
path="pulse/data/top/user/country/india/state/"
Top_user_state_list=os.listdir(path)

for state in Top_user_state_list:
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
                                # Check if the data is a list
                                if isinstance(D['data'][entity_type], list):
                                    # Iterate through the list
                                    for entity_data in D['data'][entity_type]:
                                        # Check for required keys before accessing
                                        if 'name' in entity_data and 'registeredUsers' in entity_data:
                                            Name=entity_data['name']
                                            registered_users=entity_data['registeredUsers']
                                            # Check if 'appOpens' key exists
                                            app_opens = entity_data['appOpens'] if 'appOpens' in entity_data else None

                                            topuser['Districts'].append(Name)
                                            topuser['Registered_users'].append(registered_users)

                                            topuser['States'].append(state)
                                            topuser['Yr'].append(year)
                                            topuser['Quater'].append(int(qtr_file.strip('.json')))
                                            topuser['Entity_type'].append(entity_type)

#Succesfully created a dataframe
Top_user=pd.DataFrame(topuser)
print(Top_user)
#<---------------------------------------------------------------------------------------->
engine = create_engine("postgresql+psycopg2://sugeetha_user:1sZvre5q7iok697JpIre1qCJiu5qJ9AV@dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com/sugeetha")

# Write DataFrame to SQL table
Top_user.to_sql('topuser', con=engine, if_exists='replace', index=False)
