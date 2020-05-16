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

days_option = [{'label': 'Monday', 'value': 0},
               {'label': 'Tuesday', 'value': 1},
               {'label': 'Wednesday', 'value': 2},
               {'label': 'Thursday', 'value': 3},
               {'label': 'Friday', 'value': 4},
               {'label': 'Saturday', 'value': 5},
               {'label': 'Sunday', 'value': 6}]

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
                    ]
                ),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="map-graph")],
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
    ],
)
def make_map_figure(shop_selector, open_days):
    if shop_selector == 'store':
        df = loc_df[loc_df['shop'] == 1]
    elif shop_selector == 'market':
        df = loc_df[loc_df['shop'] == 0]
    else:
        df = loc_df

    #Select only the stores that are opened
    open_days_int = list(map(lambda x : int(x), open_days))
    df['is_open'] = list(map(lambda x: not set(x).isdisjoint(open_days_int), df['day']))

    df = df[df['is_open']]

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


if __name__ == "__main__":
    app.run_server(debug=True)
