
!pip install dash

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page to scrape (e.g., country-specific reports)
url = 'https://www.ohchr.org/en/countries'
response = requests.get(url)

# Parse the page content
soup = BeautifulSoup(response.content, 'html.parser')

# Identify the table or list containing the reports
# You need to inspect the webpage's HTML structure to locate the specific container (e.g., a table, div, or ul)

# Assuming it's a table, this example extracts the data from the table
table = soup.find('table')  # Find the first table on the page

# Extract headers from the table (if present)
headers = [header.text for header in table.find_all('th')]

# Extract data rows from the table
rows = table.find_all('tr')

# Store the data in a list
data = []
for row in rows:
    cols = row.find_all('td')
    cols = [col.text.strip() for col in cols]  # Clean up the text
    data.append(cols)

# Convert the data to a Pandas DataFrame for analysis
df = pd.DataFrame(data, columns=headers)

# Save the scraped data to a CSV file
df.to_csv('un_human_rights_data.csv', index=False)

# Preview the DataFrame
print(df.head())

import pandas as pd

# Example DataFrame for human rights violations
data = {
    "Country": ["Brazil", "China", "Russia", "Brazil", "India"],
    "Violation_Type": ["Censorship", "Torture", "Political Imprisonment", "Police Brutality", "Religious Repression"],
    "Severity": ["Medium", "High", "High", "Medium", "Low"],
    "Date": ["2024-01-15", "2024-03-22", "2024-02-18", "2024-05-01", "2024-04-12"]
}

df = pd.DataFrame(data)

# Preprocessing: Standardizing and sorting data
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date', ascending=False)

# Output cleaned data
print(df)

import plotly.express as px

# Sample DataFrame with human rights violation severity by country
data = {
    'Country': ['Brazil', 'China', 'Russia', 'India', 'United States'],
    'Violations': [25, 50, 40, 35, 20]  # Number of reported violations
}
df = pd.DataFrame(data)

# Create a choropleth map
fig = px.choropleth(df,
                    locations="Country",
                    locationmode='country names',
                    color="Violations",
                    color_continuous_scale="Reds",
                    title="Human Rights Violations by Country")
fig.show()

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Sample data for human rights violations
data = {
    "Country": ["Brazil", "China", "Russia", "India", "United States"],
    "Violations": [25, 50, 40, 35, 20],
    "Date": pd.to_datetime(["2024-01-01", "2024-01-15", "2024-02-01", "2024-02-15", "2024-03-01"])
}

df = pd.DataFrame(data)

# Create Dash app
app = dash.Dash(__name__)

# Layout for the dashboard
app.layout = html.Div([
    dcc.DatePickerRange(
        id='date-picker',
        start_date=df['Date'].min(),
        end_date=df['Date'].max(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Graph(id='violation-map'),
])

# Callback to update map based on date range
@app.callback(
    Output('violation-map', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_map(start_date, end_date):
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    fig = px.choropleth(filtered_df,
                        locations="Country",
                        locationmode='country names',
                        color="Violations",
                        color_continuous_scale="Reds",
                        title="Human Rights Violations by Country")
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
