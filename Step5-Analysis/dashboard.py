import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from typing import List, Tuple 
import requests

# Load data from the provided URL
# data_url = "https://raw.githubusercontent.com/ozkary/data-engineering-mta-turnstile/main/Step5-Analysis/analysis_data.csv"
data = pd.read_csv('./analysis_data.csv', iterator=False)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB,dbc.icons.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div([
    html.H4("MTA Turnstile Data Dashboard"),
        
    dcc.DatePickerRange(
        id='date-range',
        start_date=data['created_dt'].min(),
        end_date=data['created_dt'].max(),
        display_format='YYYY-MM-DD'
    ),
 
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.P("Total Entries"),
                    html.H5(id='total-entries')
                ]),
                className='score-card'
            ),
            width=6
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.P("Total Exits"),
                    html.H5(id='total-exits')
                ]),
                className='score-card'
            ),
            width=6
        )
    ], className='score-cards'),

    dbc.Row([
            dbc.Col(
                dcc.Graph(id='top-entries-stations', className='donut-chart'),
                width=6
            ),
            dbc.Col(
                dcc.Graph(id='top-exits-stations', className='donut-chart'),
                width=6
            )
    ], className='donut-charts'),

    dbc.Row([
                dbc.Col(
                    dcc.Graph(id='exits-by-day', className='bar-chart'),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(id='entries-by-day', className='bar-chart'),
                    width=6
                )
    ], className='bar-charts'),

    dbc.Row([
                dbc.Col(
                    dcc.Graph(id='exits-by-time', className='bar-chart'),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(id='entries-by-time', className='bar-chart'),
                    width=6
                )
    ], className='bar-charts')

])

# Callback to update the score cards based on selected date range
@app.callback(
     [Output('total-entries', 'children'),
     Output('total-exits', 'children'),
     Output('top-entries-stations', 'figure'),
     Output('top-exits-stations', 'figure'),
     Output('exits-by-day', 'figure'),
     Output('entries-by-day', 'figure'),
     Output('exits-by-time', 'figure'),
     Output('entries-by-time', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)

def update_dashboard(start_date, end_date):
    filtered_data = data[(data['created_dt'] >= start_date) & (data['created_dt'] <= end_date)]   
        
    total_entries = filtered_data['entries'].sum() / 1e12  # Convert to trillions
    total_exits = filtered_data['exits'].sum() / 1e12  # Convert to trillions
      
    measures = ['exits','entries']    
    filtered_data["created_dt"] = pd.to_datetime(filtered_data['created_dt'])  
    measures = ['exits','entries']  
    
    exits_chart , entries_chart = create_station_donut_chart(filtered_data)
    exits_chart_by_day ,entries_chart_by_day = create_day_bar_chart(filtered_data, measures)
    exits_chart_by_time, entries_chart_by_time = create_time_bar_chart(filtered_data, measures)
    
    return (
        f"{total_entries:.2f}T",
        f"{total_exits:.2f}T",
        entries_chart,
        exits_chart,
        exits_chart_by_day,
        entries_chart_by_day,
        exits_chart_by_time,
        entries_chart_by_time
    )

def create_station_donut_chart(df: pd.DataFrame ) -> Tuple[go.Figure, go.Figure]:
    """
     creates the station distribution donut chart   
    """
    top_entries_stations = df.groupby('station_name').agg({'entries': 'sum'}).nlargest(10, 'entries')
    top_exits_stations = df.groupby('station_name').agg({'exits': 'sum'}).nlargest(10, 'exits')
    
    entries_chart = px.pie(top_entries_stations, names=top_entries_stations.index, values='entries',
                           title='Top 10 Stations by Entries', hole=0.3)
    exits_chart = px.pie(top_exits_stations, names=top_exits_stations.index, values='exits',
                         title='Top 10 Stations by Exits', hole=0.3)
    
    entries_chart.update_traces(marker=dict(colors=px.colors.qualitative.Plotly))
    exits_chart.update_traces(marker=dict(colors=px.colors.qualitative.Plotly))
    return entries_chart, exits_chart


def create_time_bar_chart(df: pd.DataFrame, measures : List[str] ) -> Tuple[go.Figure, go.Figure]:

    """
    Creates a bar chart using the time slot category
    """
   
    # Define time (hr) slots
    time_slots = {
        '12:00-3:59am': (0, 3, 0),
        '04:00-7:59am': (4, 7, 1),
        '08:00-11:59am': (8, 11, 2),
         '12:00-3:59pm': (12, 15, 3),
        '04:00-7:59pm': (16, 19, 4),
        '08:00-11:59pm': (20, 23, 5)
    }
        
    # Add a new column 'time_slot' based on time ranges
    def categorize_time(row):
        for slot, (start, end, order) in time_slots.items():
            if start <= row.hour <= end:
                return slot
            
    df['time_slot'] = df['created_dt'].apply(categorize_time)
    group_by_time = df.groupby('time_slot', as_index=False)[measures].sum()

    # Sort the grouped_data DataFrame based on the sorting value
    group_by_time_sorted = group_by_time.sort_values(by=['time_slot'], key=lambda x: x.map({slot: sort_order for slot, (_, _, sort_order) in time_slots.items()}))

        
    exits_chart_by_time = px.bar(group_by_time_sorted, x='time_slot', y='exits', color='time_slot',
                                title='Exits by Day of the Week', labels={'time_slot': 'Time of Day', 'exits': 'Exits'},
                                color_discrete_sequence=['green'])
    
    entries_chart_by_time = px.bar(group_by_time_sorted, x='time_slot', y='entries', color='time_slot',
                                  title='Entries by Day of the Week', labels={'time_slot': 'Time of Day', 'entries': 'Entries'},
                                  color_discrete_sequence=['orange'])
    # Hide the legend on the side
    exits_chart_by_time.update_layout(showlegend=False)
    entries_chart_by_time.update_layout(showlegend=False)

    return exits_chart_by_time, entries_chart_by_time

def create_day_bar_chart(df: pd.DataFrame, measures: List[str]) -> Tuple[go.Figure, go.Figure]:
    """
    Creates a bar chart using the week days from the given dataframe.
    """
    measures = ['exits','entries']
    day_categories = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']   
    group_by_date = df.groupby(["created_dt"], as_index=False)[measures].sum()
    
    df['weekday'] = pd.Categorical(df['created_dt'].dt.strftime('%a'),
                                                 categories=day_categories,
                                                 ordered=True)        
       
    group_by_weekday =  df.groupby('weekday', as_index=False)[measures].sum()
       
    exits_chart_by_day = px.bar(group_by_weekday, x='weekday', y='exits', color='weekday',
                                title='Exits by Day of the Week', labels={'weekday': 'Day of the Week', 'exits': 'Exits'},
                                color_discrete_sequence=['green'])
    
    entries_chart_by_day = px.bar(group_by_weekday, x='weekday', y='entries', color='weekday',
                                  title='Entries by Day of the Week', labels={'weekday': 'Day of the Week', 'entries': 'Entries'},
                                  color_discrete_sequence=['orange'])
    
    # Hide the legend on the side
    exits_chart_by_day.update_layout(showlegend=False)
    entries_chart_by_day.update_layout(showlegend=False)   

    # Return the chart
    return exits_chart_by_day, entries_chart_by_day
    

if __name__ == '__main__':
    app.run_server(debug=True)
