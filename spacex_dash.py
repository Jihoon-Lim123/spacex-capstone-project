# SpaceX Launch Dashboard using Dash and Plotly

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import urllib.request

# Download CSV if not present
csv_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
csv_filename = "spacex_launch_dash.csv"
try:
    urllib.request.urlretrieve(csv_url, csv_filename)
    print(f"{csv_filename} downloaded successfully.")
except Exception as e:
    print(f"Error downloading CSV: {e}")

# Read the SpaceX launch data
spacex_df = pd.read_csv(csv_filename)

# Extract max and min payload for slider
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center'}),

    # Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    # Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # Payload slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(x): str(int(x)) for x in range(int(min_payload), int(max_payload) + 1, 2000)},
        value=[min_payload, max_payload]
    ),

    # Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter'))
])

# Callback for pie chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(spacex_df, names='Launch Site', values='class', title='Total Success Launches by Site')
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        fig = px.pie(site_data, names='class', title=f"Success vs. Failure for site {selected_site}")
    return fig

# Callback for scatter plot
@app.callback(
    Output('success-payload-scatter', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]

    if selected_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Correlation Between Payload and Success for All Sites')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Correlation Between Payload and Success for {selected_site}')
    return fig

# Run app
if __name__ == '__main__':
    app.run(debug=True)
