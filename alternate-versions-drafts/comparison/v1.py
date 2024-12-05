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
selected_companies = st.sidebar.multiselect('Select up to 5 companies', company_list, default=company_list[:1])

# Ensure no more than 5 companies are selected
if len(selected_companies) > 5:
    st.sidebar.error("Please select up to 5 companies.")
else:
    # Filter data for selected companies
    companies_data = data[data['Company Name'].isin(selected_companies)]

    # Main Pane
    st.title('Monetized Emissions Data Explorer')

    # Graph
    st.subheader('Financial Impact of Emissions')
    fig, ax = plt.subplots(figsize=(12, 8))

    colors = ['blue', 'orange', 'green', 'red', 'purple']
    bar_width = 0.25
    index = range(len(selected_companies))

    for i, company in enumerate(selected_companies):
        company_data = companies_data[companies_data['Company Name'] == company].iloc[0]
        ebitda = company_data['EBITDA'] / 1_000_000_000
        ebitda_after_emissions = company_data['EBITDA Minus Total Monetized Emissions'] / 1_000_000_000
        monetized_emissions = company_data['Monetized Total Emissions'] / 1_000_000_000

        ax.bar([x + i * bar_width for x in index], 
               [ebitda, ebitda_after_emissions, monetized_emissions], 
               width=bar_width, 
               label=company, 
               color=colors[i])

    ax.set_ylabel('Billions of USD')
    ax.set_title('Financial Impact of Emissions for Selected Companies')
    ax.set_xticks([x + bar_width * 2 for x in index])
    ax.set_xticklabels(selected_companies, rotation=45)
    ax.legend()
    st.pyplot(fig)

    # Emissions Intensity
    st.subheader('Emissions Intensity')
    for company in selected_companies:
        company_data = companies_data[companies_data['Company Name'] == company].iloc[0]
        st.write(f"**{company}**")
        st.metric(label='Emissions Intensity Ratio', value=f'{company_data["Emissions Intensity Ratio"]:.2f}')
        st.metric(label='Emissions Intensity Percentage', value=f'{company_data["Emissions Intensity Percentage"]:.2f}%')
        st.write('---')

    # Data Table
    st.subheader('Company Data')
    for company in selected_companies:
        st.write(f"**{company}**")
        company_data = companies_data[companies_data['Company Name'] == company].iloc[0]

        monetized_emissions_data = {
            'Monetized Scope 1 & 2 Emissions': format_currency(company_data['Monetized Scope 1 & 2 Emissions']),
            'Monetized Scope 3 Emissions': format_currency(company_data['Scope Three Emissions'] * 236 * 1_000_000),  # Assuming monetization rate of $236 per ton
            'Monetized Total Emissions': format_currency(company_data['Monetized Total Emissions']),
        }

        ebitda_data = {
            'EBITDA': format_currency(company_data['EBITDA']),
            'EBITDA Minus Total Monetized Emissions': format_currency(company_data['EBITDA Minus Total Monetized Emissions']),
        }

        monetized_emissions_df = pd.DataFrame({
            'Monetized Emissions Data': monetized_emissions_data.keys(),
            'Monetized Emissions Values': monetized_emissions_data.values()
        })

        ebitda_df = pd.DataFrame({
            'EBITDA Data': ebitda_data.keys(),
            'EBITDA Values': ebitda_data.values()
        })

        data_table = pd.concat([monetized_emissions_df, ebitda_df], axis=1)
        st.table(data_table)

    # CSV Row
    st.subheader('CSV Row')
    for company in selected_companies:
        company_data = companies_data[companies_data['Company Name'] == company].iloc[0]
        csv_row = ','.join([str(company_data[col]) for col in data.columns])
        csv_row_with_header = ','.join(data.columns) + '\n' + csv_row
        st.text_area(label=f'Copy CSV Row for {company}', value=csv_row_with_header, height=100)

    # Notes Section
    st.sidebar.markdown('## Notes')
    st.sidebar.markdown('**Developed by Daniel Rosehill** ([danielrosehill.com](http://danielrosehill.com))')
    st.sidebar.markdown('**Monetization Rate**: $236 per ton of CO2 equivalents, as recommended by the International Foundation for Valuing Impact (IFVI).')
    st.sidebar.markdown('**Disclaimer**: While every effort was made to ensure data accuracy, no legal warranty is offered.')