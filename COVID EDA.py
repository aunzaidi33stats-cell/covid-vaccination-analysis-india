import pandas as pd

# Load dataset
df =pd.read_csv(
    r"C:\Users\MOHAMMAD ASHAR ZAIDI\Desktop\Covid Vaccination Dataset\statewise_vaccination_timeseries.csv"
)

# Columns to clean
numeric_cols = ['First_Dose', 'Second_Dose', 'Daily_First_dose']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col] = df[col].apply(lambda x: max(x, 0) if pd.notnull(x) else 0)

# Fix Total Vaccinations (cumulative sum of both doses)
df['Total_Vaccinations'] = df['First_Dose'] + df['Second_Dose']

# Save cleaned dataset
df.to_csv(r"C:\Users\MOHAMMAD ASHAR ZAIDI\Desktop\Aun Zaidi\vaccination_cleaned.csv", index=False)

# Check result
print("\n✅ Cleaned dataset saved with corrected Total_Vaccinations")
print(df[['State', 'Date', 'First_Dose', 'Second_Dose', 'Total_Vaccinations']].head(10))

print("Summary of cleaned dataset:")
print(df[['First_Dose', 'Second_Dose', 'Total_Vaccinations', 'Daily_First_dose']].describe())

print("\nMax values per column:")
print(df[['First_Dose', 'Second_Dose', 'Total_Vaccinations', 'Daily_First_dose']].max())

# Aggregate total vaccinations by state
state_totals = df.groupby("State")[["First_Dose", "Second_Dose", "Total_Vaccinations"]].max().reset_index()

print(state_totals.head())

# Step 2: Add population data for each state/UT
state_population = {
    "AN": 380581,      # Andaman & Nicobar Islands
    "AP": 53903393,    # Andhra Pradesh
    "AR": 1570458,     # Arunachal Pradesh
    "AS": 35607039,    # Assam
    "BR": 124799926,   # Bihar
    "CH": 1158473,     # Chandigarh
    "CT": 29436231,    # Chhattisgarh
    "DL": 18710922,    # Delhi
    "DN": 585764,      # Dadra & Nagar Haveli and Daman & Diu
    "GA": 1542750,     # Goa
    "GJ": 63872399,    # Gujarat
    "HP": 7307136,     # Himachal Pradesh
    "HR": 28204692,    # Haryana
    "JH": 38593948,    # Jharkhand
    "JK": 13606320,    # Jammu & Kashmir
    "KA": 67562686,    # Karnataka
    "KL": 35699443,    # Kerala
    "LA": 289023,      # Ladakh
    "LD": 64473,       # Lakshadweep
    "MH": 123144223,   # Maharashtra
    "ML": 3366710,     # Meghalaya
    "MN": 3091545,     # Manipur
    "MP": 85358965,    # Madhya Pradesh
    "MZ": 1239244,     # Mizoram
    "NL": 2249695,     # Nagaland
    "OD": 46356334,    # Odisha
    "PB": 30141373,    # Punjab
    "PY": 1413542,     # Puducherry
    "RJ": 81032689,    # Rajasthan
    "SK": 690251,      # Sikkim
    "TN": 77841267,    # Tamil Nadu
    "TG": 39362732,    # Telangana
    "TR": 4169794,     # Tripura
    "UP": 237882725,   # Uttar Pradesh
    "UT": 11250858,    # Uttarakhand
    "WB": 99609303     # West Bengal
}

# Map population to state_totals
state_totals["Population"] = state_totals["State"].map(state_population)

# Calculate percentages
state_totals["%_FirstDose"] = (state_totals["First_Dose"] / state_totals["Population"]) * 100
state_totals["%_SecondDose"] = (state_totals["Second_Dose"] / state_totals["Population"]) * 100
state_totals["%_FullyVaccinated"] = (state_totals["Second_Dose"] / state_totals["Population"]) * 100

print(state_totals.head())

# Top 5 states by fully vaccinated %
top_states = state_totals.sort_values("%_FullyVaccinated", ascending=False).head(5)

# Bottom 5 states by fully vaccinated %
bottom_states = state_totals.sort_values("%_FullyVaccinated", ascending=True).head(5)

print("Top 5 states by % fully vaccinated:\n", top_states[["State", "%_FullyVaccinated"]])
print("\nBottom 5 states by % fully vaccinated:\n", bottom_states[["State", "%_FullyVaccinated"]])

import matplotlib.pyplot as plt

# Sort by % fully vaccinated
plot_data = state_totals.sort_values("%_FullyVaccinated", ascending=False)

plt.figure(figsize=(14,6))
plt.bar(plot_data["State"], plot_data["%_FullyVaccinated"], color="royalblue")
plt.xticks(rotation=90)
plt.xlabel("State/UT")
plt.ylabel("% Fully Vaccinated")
plt.title("COVID-19 Vaccination Coverage by State (India)")
plt.show()


import matplotlib.pyplot as plt

# --- Step 1: Cap percentages at 100% ---
state_totals["%_FullyVaccinated"] = state_totals["%_FullyVaccinated"].clip(upper=100)

# --- Step 2: Sort and pick Top 10 / Bottom 10 ---
top10_pct = state_totals.sort_values("%_FullyVaccinated", ascending=False).head(10)
bottom10_pct = state_totals.sort_values("%_FullyVaccinated", ascending=True).head(10)

# --- Step 3: Plot ---
fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharex=True)

# Left: Top 10
axes[0].barh(top10_pct["State"], top10_pct["%_FullyVaccinated"], color="blue")
axes[0].set_title("Top 10 States by % Fully Vaccinated")
axes[0].set_xlabel("% Fully Vaccinated")
axes[0].set_xlim(0, 100)  # force limit to 100%

# Right: Bottom 10
axes[1].barh(bottom10_pct["State"], bottom10_pct["%_FullyVaccinated"], color="orange")
axes[1].set_title("Bottom 10 States by % Fully Vaccinated")
axes[1].set_xlabel("% Fully Vaccinated")
axes[1].set_xlim(0, 100)  # force limit to 100%

plt.tight_layout()
plt.show()

df["Date"] = pd.to_datetime(df["Date"])

# Daily totals across all states
daily_vaccinations = df.groupby("Date")[["First_Dose", "Second_Dose", "Total_Vaccinations"]].sum().reset_index()
print(daily_vaccinations.head())

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(daily_vaccinations["Date"], daily_vaccinations["Total_Vaccinations"], label="Total Vaccinations", color="blue")
plt.plot(daily_vaccinations["Date"], daily_vaccinations["First_Dose"], label="First Dose", color="green")
plt.plot(daily_vaccinations["Date"], daily_vaccinations["Second_Dose"], label="Second Dose", color="red")

plt.title("Vaccination Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Doses")
plt.legend()
plt.show()


# First, aggregate by date (sum over states)
df_datewise = df.groupby("Date")[["First_Dose", "Second_Dose"]].sum().reset_index()

# Now compute daily doses
df_datewise["Daily_First"] = df_datewise["First_Dose"].diff()
df_datewise["Daily_Second"] = df_datewise["Second_Dose"].diff()

# Remove negative values (caused by corrections in reporting)
df_datewise["Daily_First"] = df_datewise["Daily_First"].clip(lower=0)
df_datewise["Daily_Second"] = df_datewise["Daily_Second"].clip(lower=0)

# Plot again
plt.figure(figsize=(12,6))
plt.plot(df_datewise["Date"], df_datewise["Daily_First"], color="green", label="First Dose")
plt.plot(df_datewise["Date"], df_datewise["Daily_Second"], color="red", label="Second Dose")

plt.title("Daily COVID-19 Vaccinations in India")
plt.xlabel("Date")
plt.ylabel("Number of Doses")
plt.legend()
plt.show()

