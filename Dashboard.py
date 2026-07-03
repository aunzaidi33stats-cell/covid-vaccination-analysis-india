import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------------------
# Load Data
# -------------------------------
df = pd.read_csv(
    r"C:\Users\MOHAMMAD ASHAR ZAIDI\Desktop\Covid Vaccination Dataset\statewise_vaccination_timeseries.csv"
)

import pandas as pd

# Convert user-selected dates to datetime
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# Apply mask
mask = (df["State"] == selected_state) & (df["Date"].between(start_date, end_date))
state_df = df[mask]
