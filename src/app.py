import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
from plotly import graph_objs as go
from plotly.graph_objs import *
import plotly.express as px

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.title = 'my_app'

# Plotly mapbox public token
token = "pk.eyJ1Ijoic2lyaW5lY2hhaG1hIiwiYSI6ImNrYTkycnRrNzBuZWgycnF2c2Z6OTJxcWcifQ.-hvKGxFnevCwRy5EKDK9VA"

# import data
loc_df = pd.read_csv('../data/loc.csv')
food_df = pd.read_csv('../data/food.csv')

days_option = [{'label': 'Monday', 'value': '0'},
               {'label': 'Tuesday', 'value': '1'},
               {'label': 'Wednesday', 'value': '2'},
               {'label': 'Thursday', 'value': '3'},
               {'label': 'Friday', 'value': '4'},
               {'label': 'Saturday', 'value': '5'},
               {'label': 'Sunday', 'value': '6'}]

food_option = [{'label': 'Rice', 'value': 'rice'},
               {'label': 'Pasta', 'value': 'pasta'},
               {'label': 'Milk', 'value': 'milk'}]

importance = [{'label': 'Lower price', 'value': 'low'},
              {'label': 'Higher price', 'value': 'high'},
              {'label': 'Average price', 'value': 'avg'},
              {'label': 'Distance', 'value': 'dist'}]

# layout of the app

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.P("Type of shop:", className="control_label"),
                        dcc.RadioItems(
                            id="shop_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Store ", "value": "store"},
                                {"label": "Market ", "value": "market"},
                            ],
                            value="all",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        html.P("Open one of the following :", className="control_label"),
                        dcc.Dropdown(
                            id="open_days",
                            options=days_option,
                            multi=True,
                            value=[i for i in range(7)],
                            className="dcc_control",
                        ),
                        html.P("What would you like to buy?", className="control_label"),
                        dcc.Dropdown(
                            id="food",
                            options=food_option,
                            multi=True,
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="importance_dropdown",
                            options=importance,
                            placeholder="Select the most important for you",
                         ),
                    ]
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="map-graph")],
                ),
                html.Div(
                    [dcc.Graph(id="rank-chart")],
                ),
            ]
        )
    ]
)


# Update the map
@app.callback(
    Output("map-graph", "figure"),
    [
        Input("shop_selector", "value"),
        Input("open_days", "value"),
        Input("food", "value"),
    ],
)
def make_map_figure(shop_selector, open_days, food):
    if shop_selector == 'store':
        df = loc_df[loc_df['shop'] == 1]
    elif shop_selector == 'market':
        df = loc_df[loc_df['shop'] == 0]
    else:
        df = loc_df

    #Select only the stores that are opened
    open_days_str = list(map(lambda x: str(x), open_days))
    df['is_open'] = list(map(lambda x: any(i in x for i in open_days_str), df['day']))
    df = df[df['is_open']]

    #Select only the stores with the food that we want
    if not type(food) == type(None):
        #counts contains the number of aliment in food that each store has
        counts = pd.DataFrame(food_df[food_df['food'].isin(list(food))]['id'].value_counts())
        #we only keep the store having all the aliments we are looking for
        df = df[df['id'].isin(counts[counts['id'] == len(list(food))].index)]

    gb = df.groupby(['shop'])
    group_name = list(set(df['shop']))
    fig = go.Figure()
    for gr in group_name:
        my_gr = gb.get_group(gr)

        fig.add_trace(go.Scattermapbox(lon=my_gr['lon'],
                                       lat=my_gr['lat'],
                                       name= 'store' if gr == 1 else 'market',
                                       mode='markers',
                                       marker=dict(size=14, color='pink' if gr == 1 else 'black',),
                                       text=my_gr['Name'],
                                       showlegend=True,
                                       ))


    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=token,
            bearing=0,
            center=dict(
                lat=49.27,
                lon=-123.12
            ),
            pitch=0,
            zoom=10
        ),
    )
    return fig


# Update the ranking
@app.callback(
    Output("rank-chart", "figure"),
    [
        Input("shop_selector", "value"),
        Input("open_days", "value"),
        Input("food", "value"),
        Input("importance_dropdown", "value")
    ],
)

def make_ranking(shop_selector, open_days, food, importance):

    if shop_selector == 'store':
        df = loc_df[loc_df['shop'] == 1]
    elif shop_selector == 'market':
        df = loc_df[loc_df['shop'] == 0]
    else:
        df = loc_df

    #Select only the stores that are opened
    open_days_str = list(map(lambda x: str(x), open_days))
    df['is_open'] = list(map(lambda x: any(i in x for i in open_days_str), df['day']))
    df = df[df['is_open']]

    #Select only the stores with the food that we want
    if not type(food) == type(None):
        #counts contains the number of aliment in food that each store has
        counts = pd.DataFrame(food_df[food_df['food'].isin(list(food))]['id'].value_counts())
        #we only keep the store having all the aliments we are looking for
        loc_select = df[df['id'].isin(counts[counts['id'] == len(list(food))].index)]
        food_select = food_df[food_df['id'].isin(counts[counts['id'] == len(list(food))].index)]
        # only keep the aliments that we want
        food_select = food_select[food_select['food'].isin(list(food))]
    else:
        loc_select = df
        food_select = food_df

    #lists to store the final price/distance for each store id
    name = []
    price = []

    gb = food_select.groupby(['Name'])
    group_id = list(set(df['Name']))
    for gr in group_id:
        name.append(gr)
        my_gr = gb.get_group(gr)
        if importance == 'low':
            price.append(my_gr['min_price'].mean())
        elif importance == 'high':
            price.append(my_gr['max_price'].mean())
        else:
            price.append(my_gr['avg_price'].mean())

    results = pd.DataFrame({'Name': name, 'price': price})
    results.sort_values(['price'], ascending=False)

    data = [
        go.Scatter(
            x=results['price'],
            y=[loc_select.shape[0] - i for i in range(loc_select.shape[0])],
            mode='markers',
            marker=dict(color='red', size=10)
        )
    ]

    # Use the 'shapes' attribute from the layout to draw the vertical lines
    layout = go.Layout(
        shapes=[dict(
            type='line',
            xref='x',
            yref='y',
            x0=0,
            y0=loc_select.shape[0] - i,
            x1=results['price'][i],
            y1=loc_select.shape[0] - i,
            line=dict(
                color='grey',
                width=3
            )
        ) for i in range(loc_select.shape[0])],
        title='Lollipop Chart'
    )

    # Plot the chart
    fig = go.Figure(data, layout)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
