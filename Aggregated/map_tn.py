#Required libraries for the program

import pandas as pd
import json
import os

from sqlalchemy import create_engine

root_folder = 'pulse/data/map/transaction/hover/country/india/state'  # Your main directory
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

                    # Extract state, year, and quarter from the file path inside the loop
                    parts = dirpath.split(os.sep)
                    # Assuming the structure is .../state/year/quarter.json,
                    # state is the second to last part, and year is the last part of dirpath
                    state = parts[-2]
                    year = parts[-1]
                    quater = filename.strip('.json')

                    # Process the collected data
                    if 'data' in data and 'hoverDataList' in data['data']:
                        for state_data in data['data']['hoverDataList']:
                            district_name = state_data['name']
                            for metric_data in state_data['metric']:
                                all_data.append([state, year, int(quater), district_name, metric_data['type'], metric_data['count'], metric_data['amount']])

                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON file: {file_path}")


# Now all_data contains data from all valid JSON files
# Filter out the original JSON data and keep only the processed rows
processed_rows = [row for row in all_data if isinstance(row, list)]

columns = ['States', 'Yr', 'Quater', 'District', 'Metric_Type', 'Count', 'Amount'] # Added the expected columns

Map_Transaction_Hover_State = pd.DataFrame(processed_rows, columns=columns)

# Display the DataFrame
print(Map_Transaction_Hover_State)
#<------------------------------------------------------------------------------------------->
engine = create_engine("postgresql+psycopg2://sugeetha_user:1sZvre5q7iok697JpIre1qCJiu5qJ9AV@dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com/sugeetha")

# Write DataFrame to SQL table
Map_Transaction_Hover_State.to_sql('maptransaction', con=engine, if_exists='replace', index=False)
