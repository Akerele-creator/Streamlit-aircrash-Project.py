import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
def load_data():
    file = 'aircrashes.csv'
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    df = df.rename(columns={'Fatalities_(air)':'Fatalities'})
    # Combine Year, Month, and Day into a single date column
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1), 
    errors='coerce')
    # Specify the new column order
    new_order = ['Date', 'Year', 'Quarter', 'Month', 'Day', 'Country/Region', 
             'Aircraft_Manufacturer', 'Aircraft', 'Location', 
             'Operator', 'Ground', 'Fatalities', 'Aboard']
    # Rearrange the DataFrame
    df = df[new_order]
    #Fill or drop missing values
    df.fillna({'Country/Region': 'Unknown'}, inplace=True)
    #Fill or drop missing values
    df.fillna({'Operator': 'Unknown'}, inplace=True)
    df.fillna({'Aircraft_Manufacturer': 'Unknown'}, inplace=True)
    df.fillna({'Aircraft': 'Unknown'}, inplace=True)
    df.fillna({"'-": 'Unknown'}, inplace=True)
    df.fillna({"10": 'Unknown'}, inplace=True)
    df.fillna({'': 'Unknown'}, inplace=True)
    df.fillna({"-": 'Unknown'}, inplace=True)
    df.fillna({"??": 'Unknown'}, inplace=True)
    # Drop unnecessary columns (example: dropping the 'Ground' column)
    return df

# load the dataset
df = load_data()


# app title
st.title("Air Crashes App")

Aircraft = df['Aircraft'].unique()
selected_Aircrafts = st.sidebar.multiselect(
                    'Choose Aircraft',
                    Aircraft,
                    [Aircraft[0],
                    Aircraft[2]
                    ])
filtered_table = df[df['Aircraft'].isin(selected_Aircrafts)]
#display metrics
 
total_aboard = df.Aboard.sum()
total_no_aircraft = df.Aircraft.count()
total_no_fatalities = df.Fatalities.sum()
total_no_ground = df.Ground.sum()
st.subheader("Calculations")
col1, col2, col3, col4= st.columns(4)

col1.metric("No Of Aircraft", total_no_aircraft)
col2.metric("Total Aboard", total_aboard)
col3.metric("No of fatalities_(air)",total_no_fatalities)
col4.metric("No of Ground",total_no_ground)
# end metrics

#display the filtered table
# specific columns
st.dataframe(filtered_table[['Date',"Country/Region",
                            "Aircraft_Manufacturer", "Aircraft", "Location", 
             "Operator","Ground","Fatalities", "Aboard" ]])

# Plot number of crashes per year
st.title('Aircraft Crashes Analysis')

# Prepare data
crashes_per_year = df['Year'].value_counts().sort_index()

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(crashes_per_year.index, crashes_per_year.values, marker='o', color='red')
ax.set_title('Number of Aircraft Crashes per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Crashes')
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)

# Count the number of crashes per country/region
crashes_by_country = df['Country/Region'].value_counts().head(15)

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 6))
crashes_by_country.plot(kind='bar', ax=ax, color='chocolate')
ax.set_title('Top 10 Countries/Regions with Highest Number of Crashes')
ax.set_xlabel('Country/Region')
ax.set_ylabel('Number of Crashes')
ax.set_xticklabels(crashes_by_country.index, rotation=45)

# Display the plot in Streamlit
st.title('Aircraft Crashes by Country/Region')
st.pyplot(fig)

# Count the number of crashes per aircraft manufacturer
crashes_by_manufacturer = df['Aircraft_Manufacturer'].value_counts().head(10)

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 6))
crashes_by_manufacturer.plot(kind='bar', ax=ax, color='green')
ax.set_title('Top 10 Aircraft Manufacturers Involved in Crashes')
ax.set_xlabel('Aircraft Manufacturer')
ax.set_ylabel('Number of Crashes')
ax.set_xticklabels(crashes_by_manufacturer.index, rotation=45, ha='right')

# Display the plot in Streamlit
st.title('Aircraft Crashes by Manufacturer')
st.pyplot(fig)

# Count the number of crashes per month
crashes_by_month = df['Month'].value_counts().sort_index()

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(12, 6))
crashes_by_month.plot(kind='bar', ax=ax, color='lightcoral')
ax.set_title('Seasonal Patterns in Aircraft Crashes')
ax.set_xlabel('Month')
ax.set_ylabel('Number of Crashes')
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

# Display the plot in Streamlit
st.title('Seasonal Patterns in Aircraft Crashes')
st.pyplot(fig)