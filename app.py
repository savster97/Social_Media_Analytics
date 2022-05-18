import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd # Read and organize data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

GROUPS = ['FB', 'PINS', 'SNAP', 'TWTR', 'ETSY']

# DATA
data = pd.read_csv("sm_stock_price_data.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
data = data[data['Date'] > '2017-06-01']
data.sort_values("Date", inplace=True)
symbol_groups = data.groupby(['Symbol'])
# Facebook
fb_data = symbol_groups.get_group('FB')
fb_dates = fb_data.groupby('Date')
fb_df = pd.DataFrame(columns=['Date', 'High', 'Low', 'Volume'])

for fb_date, fb_dataset in fb_dates:
    fb_new_row = pd.DataFrame([{'Date': fb_date, 'High': fb_dataset['High'].mean(), 
                                'Low': fb_dataset['Low'].mean(), 
                                'Volume': fb_dataset['Volume'].mean()}])
    fb_df = pd.concat([fb_df, fb_new_row])
# PINS
pins_data = symbol_groups.get_group('PINS')
pins_dates = pins_data.groupby('Date')
pins_df = pd.DataFrame(columns=['Date', 'High', 'Low', 'Volume'])

for pins_date, pins_dataset in pins_dates:
    pins_new_row = pd.DataFrame([{'Date': pins_date, 'High': pins_dataset['High'].mean(), 
                                'Low': pins_dataset['Low'].mean(), 
                                'Volume': pins_dataset['Volume'].mean()}])
    pins_df = pd.concat([pins_df, pins_new_row])

# SNAP
snap_data = symbol_groups.get_group('SNAP')
snap_dates = snap_data.groupby('Date')
snap_df = pd.DataFrame(columns=['Date', 'High', 'Low', 'Volume'])

for snap_date, snap_dataset in snap_dates:
    snap_new_row = pd.DataFrame([{'Date': snap_date, 'High': snap_dataset['High'].mean(), 
                                'Low': snap_dataset['Low'].mean(), 
                                'Volume': snap_dataset['Volume'].mean()}])
    snap_df = pd.concat([snap_df, snap_new_row])

# TWTR
twtr_data = symbol_groups.get_group('TWTR')
twtr_dates = twtr_data.groupby('Date')
twtr_df = pd.DataFrame(columns=['Date', 'High', 'Low', 'Volume'])

for twtr_date, twtr_dataset in twtr_dates:
    twtr_new_row = pd.DataFrame([{'Date': twtr_date, 'High': twtr_dataset['High'].mean(), 
                                'Low': twtr_dataset['Low'].mean(), 
                                'Volume': twtr_dataset['Volume'].mean()}])
    twtr_df = pd.concat([twtr_df, twtr_new_row])

# ETSY
etsy_data = symbol_groups.get_group('ETSY')
etsy_dates = etsy_data.groupby('Date')
etsy_df = pd.DataFrame(columns=['Date', 'High', 'Low', 'Volume'])

for etsy_date, etsy_dataset in etsy_dates:
    etsy_new_row = pd.DataFrame([{'Date': etsy_date, 'High': etsy_dataset['High'].mean(), 
                                'Low': etsy_dataset['Low'].mean(), 
                                'Volume': etsy_dataset['Volume'].mean()}])
    etsy_df = pd.concat([etsy_df, etsy_new_row])

# APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
app.layout = html.Div(id='sma',
        style={'backgroundColor': colors['background']},
        children=[
        html.H1(children="Social Media Stock Data 2017-2020",
        style={
            'textAlign': 'center',
            'color': 'white'
        }),
        html.P(
            children="Analyze the behavior of social media stocks between the years 2017-2020.",
            style={
            'textAlign': 'center',
            'color': 'white'
        }
        ),
        dcc.Slider(
            id='year-slider',
            min=2017,
            max=2020,
            value=2017,
            marks={key: str(key) for key in range(2021)},
            step=1
        ),
        dcc.Graph(id='volume-graph',
            figure={
                "data": [
                    {
                        "x": fb_df['Date'],
                        "y": fb_df['Volume'],
                        "type": "lines",
                        "name": "Facebook"
                    },
                    {
                        "x": pins_df['Date'],
                        "y": pins_df['Volume'],
                        "type": "lines",
                        "name": "Pinterest"
                    },
                    {
                        "x": snap_df['Date'],
                        "y": snap_df['Volume'],
                        "type": "lines",
                        "name": "Snapchat"
                    },
                    {
                        "x": twtr_df['Date'],
                        "y": twtr_df['Volume'],
                        "type": "lines",
                        "name": "Twitter"
                    },
                    {
                        "x": etsy_df['Date'],
                        "y": etsy_df['Volume'],
                        "type": "lines",
                        "name": "Etsy"
                    }
                ],
                "layout": {
                    "title": "Stock Volume",
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                    'color': 'white'
                    },
                    'xaxis':{
                        'title':'Date'
                    },
                    'yaxis':{
                        'title':'Average Volume of Shares'
                    }   
                },
            },
        ),
        html.P(
            'Select Social Media Type:', className = 'fix_label', style = {'color': 'white', 'text-align': 'center'}),
        dcc.RadioItems(id = 'radio_items',
            labelStyle = {"display": "inline-block"},
            value = 'TWTR',
            options = [{'label': i, 'value': i} for i in ['Facebook', 'Pinterest', 'Snapchat', 'Twitter', 'Etsy']],
            style = {'color': 'white', 'text-align': 'center'}),
        dcc.Graph(id='high-low-graph',
            figure={
                "data": [
                    {
                        "x": fb_df['Date'],
                        "y": fb_df['High'],
                        "type": "lines",
                        "name": "Average High"
                    },
                    {
                        "x": fb_df['Date'],
                        "y": fb_df['Low'],
                        "type": "lines",
                        "name": "Average Low"
                    },
                ],
                "layout": {
                    'title':'Stock Prices by Date',
                'xaxis':{
                    'title':'Date'
                },
                'yaxis':{
                     'title':'Stock Price USD'
                },
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': 'white'
                }
            }
            },
        ),
    ]
)

@app.callback(
    Output('volume-graph', 'figure'),
    [Input('year-slider', 'value')]
)

def update_figure(slider_value):
    selected_year = int(slider_value)
    figure={
                "data": [
                    {
                        "x": fb_df['Date'][pd.DatetimeIndex(fb_df['Date']).year <= selected_year],
                        "y": fb_df['Volume'][pd.DatetimeIndex(fb_df['Date']).year <= selected_year],
                        "type": "lines",
                        "name": "Facebook"
                    },
                    {
                        "x": pins_df['Date'][pd.DatetimeIndex(pins_df['Date']).year <= selected_year],
                        "y": pins_df['Volume'][pd.DatetimeIndex(pins_df['Date']).year <= selected_year],
                        "type": "lines",
                        "name": "Pinterest"
                    },
                    {
                        "x": snap_df['Date'][pd.DatetimeIndex(snap_df['Date']).year <= selected_year],
                        "y": snap_df['Volume'][pd.DatetimeIndex(snap_df['Date']).year <= selected_year],
                        "type": "lines",
                        "name": "Snapchat"
                    },
                    {
                        "x": twtr_df['Date'][pd.DatetimeIndex(twtr_df['Date']).year <= selected_year],
                        "y": twtr_df['Volume'][pd.DatetimeIndex(twtr_df['Date']).year <= selected_year],
                        "type": "lines",
                        "name": "Twitter"
                    },
                    {
                        "x": etsy_df['Date'][pd.DatetimeIndex(etsy_df['Date']).year <= selected_year],
                        "y": etsy_df['Volume'][pd.DatetimeIndex(etsy_df['Date']).year <= selected_year],
                        "type": "lines",
                        "name": "Etsy"
                    }
                ],
                "layout": {
                    "title": "Stock Volume by Date",
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                    'color': 'white'
                    },
                    'xaxis':{
                        'title':'Date'
                    },
                    'yaxis':{
                        'title':'Average Volume of Shares'
                    }   
                },
            }
    return figure

@app.callback(
    Output('high-low-graph', 'figure'),
    [Input('radio_items', 'value')]
)

def update_figure_2(sm_type):
    if sm_type == 'Facebook':
        figure= {
                    "data": [
                        {
                            "x": fb_df['Date'],
                            "y": fb_df['High'],
                            "type": "lines",
                            "name": "Average High"
                        },
                        {
                            "x": fb_df['Date'],
                            "y": fb_df['Low'],
                            "type": "lines",
                            "name": "Average Low"
                        }
                    ],
                    "layout": {
                        'title':'Stock Prices by Date',
                        'xaxis':{
                            'title':'Date'
                        },
                        'yaxis':{
                            'title':'Stock Price USD'
                        },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': 'white'
                        }
                }
            }
    elif sm_type == 'Pinterest':
        figure= {
                    "data": [
                        {
                            "x": pins_df['Date'],
                            "y": pins_df['High'],
                            "type": "lines",
                            "name": "Average High"
                        },
                        {
                            "x": pins_df['Date'],
                            "y": pins_df['Low'],
                            "type": "lines",
                            "name": "Average Low"
                        }
                    ],
                    "layout": {
                        'title':'Stock Prices by Date',
                        'xaxis':{
                            'title':'Date'
                        },
                        'yaxis':{
                            'title':'Stock Price USD'
                        },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': 'white'
                        }
                    }
                }
    elif sm_type == 'Snapchat':
        figure= {
                    "data": [
                        {
                            "x": snap_df['Date'],
                            "y": snap_df['High'],
                            "type": "lines",
                            "name": "Average High"
                        },
                        {
                            "x": snap_df['Date'],
                            "y": snap_df['Low'],
                            "type": "lines",
                            "name": "Average Low"
                        }
                    ],
                    "layout": {
                        'title':'Stock Prices by Date',
                        'xaxis':{
                            'title':'Date'
                        },
                        'yaxis':{
                            'title':'Stock Price USD'
                        },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': 'white'
                        }
                    }
                }
    elif sm_type == 'Twitter':
        figure= {
                    "data": [
                        {
                            "x": twtr_df['Date'],
                            "y": twtr_df['High'],
                            "type": "lines",
                            "name": "Average High"
                        },
                        {
                            "x": twtr_df['Date'],
                            "y": twtr_df['Low'],
                            "type": "lines",
                            "name": "Average Low"
                        }
                    ],
                    "layout": {
                        'title':'Stock Prices by Date',
                        'xaxis':{
                            'title':'Date'
                        },
                        'yaxis':{
                            'title':'Stock Price USD'
                        },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': 'white'
                        }
                    }
                }
    elif sm_type == 'Etsy':
        figure= {
                    "data": [
                        {
                            "x": etsy_df['Date'],
                            "y": etsy_df['High'],
                            "type": "lines",
                            "name": "Average High"
                        },
                        {
                            "x": etsy_df['Date'],
                            "y": etsy_df['Low'],
                            "type": "lines",
                            "name": "Average Low"
                        }
                    ],
                    "layout": {
                        'title':'Stock Prices by Date',
                        'xaxis':{
                            'title':'Date'
                        },
                        'yaxis':{
                            'title':'Stock Price USD'
                        },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': 'white'
                        }
                    }
                }
    else:
        figure= {
                    "data": [
                        {
                            "x": pins_df['Date'],
                            "y": pins_df['High'],
                            "type": "lines",
                            "name": "Average High"
                        },
                        {
                            "x": pins_df['Date'],
                            "y": pins_df['Low'],
                            "type": "lines",
                            "name": "Average Low"
                        }
                    ],
                    "layout": {
                        'title':'Stock Prices by Date',
                        'xaxis':{
                            'title':'Date'
                        },
                        'yaxis':{
                            'title':'Stock Price USD'
                        },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': 'white'
                        }
                    }
                }

    return figure

if __name__ == "__main__":
    app.run_server(debug=True)

