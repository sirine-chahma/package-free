import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd
from plotly import graph_objs as go
from plotly.graph_objs import *



app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

#import data
loc_df = pd.read_csv('../data/loc.csv')

#layout of the app

app.layout = html.Div(className="map",
                    children=[
                        dcc.Graph(id="map-graph"),
                        ],
                    )

#Map
@app.callback(
    Output("map-graph", "figure"),
)
def update_graph():
    zoom = 12.0
    latInitial = 1
    lonInitial = 1
    bearing = 0


    return go.Figure(
        data=[
            # Plot of important locations on the map
            Scattermapbox(
                lat=[1, 2],
                lon=[1, 2],
                mode="markers",
                hoverinfo="text",
                text=[name for name in loc_df['Name']],
                marker=dict(size=8, color="#ffa0a0"),
            ),
        ],
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=35, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=latInitial, lon=lonInitial), 
                style="dark",
                bearing=bearing,
                zoom=zoom,
            ),
            updatemenus=[
                dict(
                    buttons=(
                        [
                            dict(
                                args=[
                                    {
                                        "mapbox.zoom": 12,
                                        "mapbox.center.lon": "1",
                                        "mapbox.center.lat": "1",
                                        "mapbox.bearing": 0,
                                        "mapbox.style": "dark",
                                    }
                                ],
                                label="Reset Zoom",
                                method="relayout",
                            )
                        ]
                    ),
                    direction="left",
                    pad={"r": 0, "t": 0, "b": 0, "l": 0},
                    showactive=False,
                    type="buttons",
                    x=0.45,
                    y=0.02,
                    xanchor="left",
                    yanchor="bottom",
                    bgcolor="#323130",
                    borderwidth=1,
                    bordercolor="#6d6d6d",
                    font=dict(color="#FFFFFF"),
                )
            ],
        ),
    )



if __name__ == "__main__":
    app.run_server(debug=True)