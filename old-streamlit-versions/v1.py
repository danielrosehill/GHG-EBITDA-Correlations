import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('emissions_data.csv')

data = load_data()

# Function to format numbers to billions
def format_currency(value):
    return f'${value / 1_000_000_000:.2f} B'

# Function to format emissions to millions of tons
def format_emissions(value):
    return f'{value / 1_000_000:.2f} M tons CO2e'

# Sidebar
st.sidebar.title('Company Selection')
company_list = sorted(data['Company Name'].unique())
selected_company = st.sidebar.selectbox('Select a company', company_list)

# Filter data for selected company
company_data = data[data['Company Name'] == selected_company].iloc[0]

# Main Pane
st.title('Monetized Emissions Data Explorer')

# Graph
st.subheader('Financial Impact of Emissions')
fig, ax = plt.subplots(figsize=(10, 6))

ebitda = company_data['EBITDA'] / 1_000_000_000
ebitda_after_emissions = company_data['EBITDA Minus Total Monetized Emissions'] / 1_000_000_000
monetized_emissions = company_data['Monetized Total Emissions'] / 1_000_000_000

ax.bar(['EBITDA', 'EBITDA after emissions', 'Monetized emissions'], 
       [ebitda, ebitda_after_emissions, monetized_emissions], 
       color=['blue', 'green', 'red'])

ax.set_ylabel('Billions of USD')
ax.set_title(f'Financial Impact of Emissions for {selected_company}')
st.pyplot(fig)

# Data Table
st.subheader('Company Data')

# Monetized Emissions Data
monetized_emissions_data = {
    'Monetized Scope 1 & 2 Emissions': format_currency(company_data['Monetized Scope 1 & 2 Emissions']),
    'Monetized Total Emissions': format_currency(company_data['Monetized Total Emissions']),
}

# EBITDA Data
ebitda_data = {
    'EBITDA': format_currency(company_data['EBITDA']),
    'EBITDA Minus Total Monetized Emissions': format_currency(company_data['EBITDA Minus Total Monetized Emissions']),
}

# Create DataFrames
monetized_emissions_df = pd.DataFrame({
    'Monetized Emissions Data': monetized_emissions_data.keys(),
    'Monetized Emissions Values': monetized_emissions_data.values()
})

ebitda_df = pd.DataFrame({
    'EBITDA Data': ebitda_data.keys(),
    'EBITDA Values': ebitda_data.values()
})

# Concatenate DataFrames side by side
data_table = pd.concat([monetized_emissions_df, ebitda_df], axis=1)

st.table(data_table)

# Emissions Intensity Ratio
st.subheader('Emissions Intensity')
emissions_intensity_data = {
    'Emissions Intensity Ratio': f'{company_data["Emissions Intensity Ratio"]:.2f}',
    'Emissions Intensity Percentage': f'{company_data["Emissions Intensity Percentage"]:.2f}%',
}

emissions_intensity_df = pd.DataFrame({
    'Data Point': emissions_intensity_data.keys(),
    'Values': emissions_intensity_data.values()
})

st.table(emissions_intensity_df)

# Notes Section
st.sidebar.markdown('## Notes')
st.sidebar.markdown('**Developed by Daniel Rosehill** ([danielrosehill.com](http://danielrosehill.com))')
st.sidebar.markdown('**Monetization Rate**: $236 per ton of CO2 equivalents, as recommended by the International Foundation for Valuing Impact (IFVI).')
st.sidebar.markdown('**Disclaimer**: While every effort was made to ensure data accuracy, no legal warranty is offered.')