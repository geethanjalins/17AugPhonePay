import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Load GeoJSON
url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
geojson = requests.get(url).json()

# Extract state names
geo_states = [feature["properties"]["ST_NM"] for feature in geojson["features"]]

# Load your dataset (update the path or use uploader)
@st.cache
def load_data():
    return pd.read_csv('C:/Users/user/OneDrive/Desktop/pro/Aggregated/states_24(4).csv')

Agg_States24_df = load_data()

# Mapping for state names
state_name_mapping = {
    'maharashtra': 'Maharashtra',
    'uttar-pradesh': 'Uttar Pradesh',
    'karnataka': 'Karnataka',
    'rajasthan': 'Rajasthan',
    'west-bengal': 'West Bengal',
    'tamil-nadu': 'Tamil Nadu',
    'bihar': 'Bihar',
    'madhya-pradesh': 'Madhya Pradesh',
    'telangana': 'Telangana',
    'andhra-pradesh': 'Andhra Pradesh',
    'kerala': 'Kerala',
    'gujarat': 'Gujarat',
    'haryana': 'Haryana',
    'assam': 'Assam',
    'jharkhand': 'Jharkhand',
    'odisha': 'Odisha',
    'himachal-pradesh': 'Himachal Pradesh',
    'chandigarh': 'Chandigarh',
    'tripura': 'Tripura',
    'jammu-and-kashmir': 'Jammu & Kashmir',
    'jammu-&-kashmir': 'Jammu & Kashmir',
    'punjab': 'Punjab',
    'sikkim': 'Sikkim',
    'uttarakhand': 'Uttarakhand',
    'nagaland': 'Nagaland',
    'meghalaya': 'Meghalaya',
    'mizoram': 'Mizoram',
    'arunachal-pradesh': 'Arunachal Pradesh',
    'manipur': 'Manipur',
    'dadra-and-nagar-haveli-and-daman-and-diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'delhi': 'Delhi',
    'andaman-and-nicobar-islands': 'Andaman & Nicobar',
    'andaman-&-nicobar-islands': 'Andaman & Nicobar',
    'ladakh': 'Ladakh',
    'puducherry': 'Puducherry',
    'goa': 'Goa',
    'chhattisgarh': 'Chhattisgarh',
    'lakshadweep': 'Lakshadweep'
}

# Replace state names
Agg_States24_df['state'] = Agg_States24_df['state'].replace(state_name_mapping)

# Optional: Show the DataFrame
st.write("Aggregated State Data 2024 Q4")
#st.dataframe(Agg_States24_df)

# Identify mismatched states
missing = set(Agg_States24_df['state']) - set(geo_states)
if missing:
    st.write("States in data not found in GeoJSON:", missing)

# Create choropleth map
fig = px.choropleth(
    Agg_States24_df,
    geojson=geojson,
    featureidkey="properties.ST_NM",
    locations="state",
    color="total_transactions",
    hover_data=["state", "total_transactions", "total_amount", "total_users"],
    color_continuous_scale="Viridis",
    title="PhonePe Transactions by State 2024 Q4"
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

# Display the map in Streamlit
st.plotly_chart(fig)
