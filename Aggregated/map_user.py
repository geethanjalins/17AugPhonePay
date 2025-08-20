#Required libraries for the program

import pandas as pd
import json
import os

from sqlalchemy import create_engine

# Base path
path = "pulse/data/map/user/hover/country/india/state"

# Collect rows here
data_list = []

# Iterate over states
for state in os.listdir(path):
    p_s = os.path.join(path, state)
    if os.path.isdir(p_s):
        # Iterate over years
        for year in os.listdir(p_s):
            p_y = os.path.join(p_s, year)
            if os.path.isdir(p_y) and year.isdigit():
                # Iterate over quarter files
                for qtr_file in os.listdir(p_y):
                    p_q = os.path.join(p_y, qtr_file)
                    if os.path.isfile(p_q) and qtr_file.endswith(".json"):
                        try:
                            with open(p_q, "r") as f:
                                D = json.load(f)

                            # Check if hoverData exists
                            if "data" in D and "hoverData" in D["data"]:
                                hover_data = D["data"]["hoverData"]
                                for district, values in hover_data.items():
                                    if (
                                        isinstance(values, dict)
                                        and "registeredUsers" in values
                                        and "appOpens" in values
                                    ):
                                        data_list.append({
                                            "States": state,
                                            "Yr": int(year),
                                            "Quarter": int(qtr_file.strip(".json")),
                                            "District": district,
                                            "Registered_users": values["registeredUsers"],
                                            "App_opens": values["appOpens"]
                                        })

                        except json.JSONDecodeError:
                            print(f"Skipping invalid JSON: {p_q}")
                        except Exception as e:
                            print(f"Error in file {p_q}: {e}")

# Create DataFrame
Map_user_hover_state = pd.DataFrame(data_list)

print(Map_user_hover_state.shape)
print(Map_user_hover_state.head())
#<------------------------------------------------------------------------------------------>
engine = create_engine("postgresql+psycopg2://sugeetha_user:1sZvre5q7iok697JpIre1qCJiu5qJ9AV@dpg-d2253mm3jp1c738gqbf0-a.singapore-postgres.render.com/sugeetha")

# Write DataFrame to SQL table
Map_user_hover_state.to_sql('mapuser', con=engine, if_exists='replace', index=False)

