# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                #jem1
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site",
                                            searchable=True
                                ),
                                #end jem1
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                #jem3
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 
                                           2500: '2500',
                                           5000: '5000',
                                           7500: '7500',
                                           10000: '10000'},
                                    value=[min_payload, max_payload]),
                                #end jem3

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
#jem2
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    # return the outcomes piechart for a selected site
    elif entered_site == 'CCAFS LC-40':
        data = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        print(data)
        fig = px.pie(data, values='class', 
        names='class', 
        title='Total Success Launches for site CCAFS LC-40')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        data = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        fig = px.pie(data, values='class', 
        names='class', 
        title='Total Success Launches for site VAFB SLC-4E')
        return fig
    elif entered_site == 'KSC LC-39A':
        data = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        fig = px.pie(data, values='class', 
        names='class', 
        title='Total Success Launches for site KSC LC-39A')
        return fig
    else:   # site is CCAFS SLC-40
        data = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        fig = px.pie(data, values='class', 
        names='class', 
        title='Total Success Launches for site CCAFS SLC-40')
        return fig
#end jem2   

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
#jem4
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_plot(entered_site,slider_range):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', 
        y='class',
        color='Booster Version Category',
        title='Correlation between payload and success for all sites')
        return fig
    # return the outcomes piechart for a selected site
    elif entered_site == 'CCAFS LC-40':
        data = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        print(data)
        fig = px.scatter(data, values='class', 
        color='Booster Version Category', 
        title='Correlation between payload and success for site CCAFS LC-40')
        return fig
    elif entered_site == 'VAFB SLC-4E':
        data = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        fig = px.scatter(data, values='class', 
        color='Booster Version Category', 
        title='Correlation between payload and success for site VAFB SLC-4E')
        return fig
    elif entered_site == 'KSC LC-39A':
        data = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        fig = px.scatter(data, values='class', 
        color='Booster Version Category', 
        title='Correlation between payload and success for site KSC LC-39A')
        return fig
    else:   # site is CCAFS SLC-40
        data = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        fig = px.scatter(data, values='class', 
        color='Booster Version Category', 
        title='Correlation between payload and success for site CCAFS SLC-40')
        return fig
#end jem4

# Run the app
if __name__ == '__main__':
    app.run_server()
