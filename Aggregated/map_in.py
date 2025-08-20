#Required libraries for the program

import pandas as pd
import json
import os

from sqlalchemy import create_engine

# ---------- 1️⃣ Extract Map_Insurance (lat/lng/metric/label) ----------
root_folder = "pulse/data/map/insurance/country/india/state/"
all_data = []

for state_name in os.listdir(root_folder):
    state_path = os.path.join(root_folder, state_name)
    if os.path.isdir(state_path):
        for year in os.listdir(state_path):
            year_path = os.path.join(state_path, year)
            if os.path.isdir(year_path) and year.isdigit():
                for filename in os.listdir(year_path):
                    if filename.endswith('.json'):
                        file_path = os.path.join(year_path, filename)
                        with open(file_path, 'r') as f:
                            try:
                                data = json.load(f)
                                if 'data' in data and 'data' in data['data']:
                                    for row in data['data']['data']:
                                        if len(row) == 4:
                                            all_data.append({
                                                'States': state_name,
                                                'Yr': int(year),
                                                'Quater': int(filename.strip('.json')),
                                                'Latitude': row[0],
                                                'Longitude': row[1],
                                                'Metric': row[2],
                                                'Label': row[3]
                                            })
                            except json.JSONDecodeError:
                                print(f"Skipping invalid JSON file: {file_path}")

Map_Insurance = pd.DataFrame(all_data)
print(Map_Insurance.head(5))
#<----------------------------------------------------------------------------------------->
Map_Insurance = pd.DataFrame(all_data)

# Create database engine
engine = create_engine("postgresql+psycopg2://sugeetha_user:1sZvre5q7iok697JpIre1qCJiu5qJ9AV@dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com/sugeetha")

# Write DataFrame to SQL table
Map_Insurance.to_sql('mapinsurance', con=engine, if_exists='replace', index=False)
