import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd

from vega_datasets import data

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
df = data.barley()



SIDEBAR_STYLE_LEFT = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "300px",
    "padding": "2rem 1rem",
    "height": "100%",
    #"background-color": "#f8f9fa",
    "background-color": '#343A40', 
    "color": 'white',
    "overflow": "auto"
}

BODY = {
  "margin-left": "300px",
  "padding": "100px 16px",
  "height": "100%",
}

_sidebar_left = dbc.Container(
    [
        html.Br(),
        
        html.H2("Barley Yield", className="display-10"),
        html.P(
            "Choose the filters to see the visualization change", className="lead"
        ),
        html.H6("Year:"),
        dcc.RadioItems(
            id='year_selector',
            options=[
                {'label': '1931', 'value': '1931'},
                {'label': '1932', 'value': '1932'},
                {'label': 'Both', 'value': 'both'}
            ],
            value='both',
            className="display-10"
        ),
        html.Hr(),
        html.H5("Site:"),
        dcc.Dropdown(
            id='site_selector',
            options=[
                {'label': site, 'value': site} for site in barley_df['site'].unique()
            ],
            value=barley_df['site'].unique(),
            className="display-10",
            multi=True,
            style={
                "color": 'black'
            },
        ),
        html.Hr(),
        html.H6("Variety:"),
        dcc.Dropdown(
            id='variety_selector',
            options=[
                {'label': variety, 'value': variety} for variety in barley_df['variety'].unique()
            ],
            value=barley_df['variety'].unique(),
            multi=True,
            style={
                "color": 'black'
            },
        ),
        html.Hr(),
        html.P(
            "More information about the dataset :", className="lead"
        ),
        html.P(
            "We ch", className="lead"
        )
    ],
    style=SIDEBAR_STYLE_LEFT,
)


_body = dbc.Container(
    [   dbc.Row(
            [dbc.Col(
                    [   html.P(
                            "Barley is paering:", className="lead"), 
                        
                        html.P(
                            "Trick : Place on!", className="lead"
                        )
                    ],
                    md=11,
                )
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([],md=2),
                dbc.Col(
                    [   
                        html.Center(html.H2("Map of the locations of the selected sites")),
                        html.Iframe(
                            sandbox='allow-scripts',
                            id='map',
                            height='400',
                            width='1000',
                            style={'border-width': '0'},
                        )
                    ],
                    md=6,
                ),
                dbc.Col(
                    [html.Br(),
                    html.Br(),
                    html.P(
                        "All the sites unit represents.", className="lead")
                    ]
                    ,md=3),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [   
                        html.P("The folleach variety.", className="lead"),
                        html.Center(html.H2("Yield per Variety")),
                        html.Iframe(
                            sandbox='allow-scripts',
                            id='plot1',
                            height='500',
                            width='500',
                            style={'border-width': '0'},
                        ),                  
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.P("The following grapsite.", className="lead"),
                        html.Center(html.H2("Yield per Site")),
                        html.Iframe(
                            sandbox='allow-scripts',
                            id='plot2',
                            height='500',
                            width='500',
                            style={'border-width': '0'},
                        ),                  
                    ],
                    md=6
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("The followired.", className="lead"),
                        html.Center(html.H2("Yields foted sites")),
                        html.Iframe(
                            sandbox='allow-scripts',
                            id='plot3',
                            height='600',
                            width='1200',
                            style={'border-width': '0'},
                        ),              
                        
                    ],
                    md=12
                ),
            ]

        )
    ],
    className="mt-4",
    style=BODY
)

@app.callback(
    Output('map', 'srcDoc'),
    [Input('site_selector', 'value')])
def make_map(site):

    if not isinstance(site, list):
        site_temp = list(site)
    else:
        site_temp = site

    #states = alt.topo_feature(vega_datasets.data.us_10m.url, feature='states')
    states = alt.topo_feature(data.us_10m.url, feature='states')
    background = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='blue'
    ).properties(
        width=500,
        height=300
    ).transform_filter((alt.datum.id == 27))

    sites = pd.DataFrame({'site': barley_df['site'].unique().tolist(),
                      'lat': [10, 0, -38, -43, 10, 18],
                      'long': [-40, -70, -30, 50, 30, 10]})

    sites_filter = sites[sites['site'].isin(site_temp)]

    points = alt.Chart(sites_filter).mark_circle(
        size=100,
        color='red'
    ).encode(
        x = alt.X('lat:Q', scale=alt.Scale(domain=[-100, 100]), axis=None),
        y = alt.Y('long:Q', scale=alt.Scale(domain=[-100, 100]), axis=None),
        tooltip = ['site']
    )

    chart = (background + points)

    return chart.to_html()

@app.callback(
    Output('plot1', 'srcDoc'),
    [Input('year_selector', 'value'), Input('site_selector', 'value'), Input('variety_selector', 'value')])
#create the plot of the yield per variety
def make_yield_per_var(year, site, variety):

    if year == 'both':
        year_temp = [1931, 1932]
    else:
        year_temp = [year]

    #create a list with the selected site(s)
    if not isinstance(site, list):
        site_temp = list(site)
    else:
        site_temp = site
    
    #create a list with the selected varieties
    if not isinstance(variety, list):
        variety_temp = list(variety)
    else:
        variety_temp = variety

    #filter the year
    df_temp = barley_df[barley_df['year'].isin(year_temp)]
    #filter the site
    df_temp = df_temp[df_temp['site'].isin(site_temp)]
    #filter the variety
    df_temp = df_temp[df_temp['variety'].isin(variety_temp)]

    #create the bar graph
    chart = alt.Chart(df_temp).mark_bar().encode(
        alt.X("variety:N", 
            title="Variety",
            axis = alt.Axis(labelAngle=45)),
        alt.Y("yield:Q",
            title = "Yield (kg/hectare)"),
        alt.Color("year:N", legend=alt.Legend(title="Year")),
        tooltip=['site', 'year', 'yield', 'variety']
        ).properties(width = 320, height=300
        ).configure_title(fontSize=18
        ).configure_axis(
            labelFontSize=14, 
            titleFontSize=18)

    return chart.to_html()

@app.callback(
    Output('plot2', 'srcDoc'),
    [Input('year_selector', 'value'), Input('site_selector', 'value'), Input('variety_selector', 'value')])
#create the plot of the yield per site
def make_yield_per_site(year, site, variety):

    #create a list with the selected year(s)
    if year == 'both':
        year_temp = [1931, 1932]
    else:
        year_temp = [year]

    #create a list with the selected site(s)
    if not isinstance(site, list):
        site_temp = list(site)
    else:
        site_temp = site
    
    #create a list with the selected varieties
    if not isinstance(variety, list):
        variety_temp = list(variety)
    else:
        variety_temp = variety

    #filter the year
    df_temp = barley_df[barley_df['year'].isin(year_temp)]

    #filter the site
    df_temp = df_temp[df_temp['site'].isin(site_temp)]

    #filter the variety
    df_temp = df_temp[df_temp['variety'].isin(variety_temp)]

    #create the bar graph
    chart = alt.Chart(df_temp).mark_bar().encode(
        alt.X("site:N", 
            title="Site",
            sort=alt.EncodingSortField(field="yield", op="sum", order='ascending'),
            axis = alt.Axis(labelAngle=45)),
        alt.Y("yield:Q",
            title = "Yield (kg/hectare)"),
        alt.Color("year:N", legend=alt.Legend(title="Year")),
        tooltip=['site', 'year', 'yield', 'variety']
    ).properties(width = 320, height=300
    ).configure_title(fontSize=18
    ).configure_axis(
        labelFontSize=14, 
        titleFontSize=18)
    
    return chart.to_html()

@app.callback(
    Output('plot3', 'srcDoc'),
    [Input('year_selector', 'value'), Input('site_selector', 'value'), Input('variety_selector', 'value')])
#create the faceted chart of the yield per variety for every site
def make_yield_per_site_per_variety(year, site, variety):

    #create a list with the selected year(s)
    if year == 'both':
        year_temp = [1931, 1932]
    else:
        year_temp = [year]

    #create a list with the selected site(s)
    if not isinstance(site, list):
        site_temp = list(site)
    else:
        site_temp = site

    #create a list with the selected varieties
    if not isinstance(variety, list):
        variety_temp = list(variety)
    else:
        variety_temp = variety
    
    #filter the year
    df_temp = barley_df[barley_df['year'].isin(year_temp)]

    #filter the variety
    df_temp = df_temp[df_temp['variety'].isin(variety_temp)]

    #my_graphs is a list that will contain all the different bar graphs that will be faceted
    my_graphs = []

    if df_temp.empty == False : 
        for sites in site_temp:
            #filter the site
            df_temp_site = df_temp[df_temp['site'] == sites]
            #create a data frame to find the maximum value of the yield
            df_max = (df_temp_site.drop(columns=['year'])
                            .groupby(['variety', 'site'])
                            .agg('sum')
                            .sort_values('yield', ascending=False)
                            .reset_index()
                    )
            #my_max is the variety that had the highest yield

            my_max = df_max['variety'][0]
                    
            #create the bar graph
            chart = alt.Chart(df_max).mark_bar().encode(
            alt.Y("variety:N", 
                title= sites,
                axis = alt.Axis(labelAngle=0)),
            alt.X("yield:Q",
                title = "Yield (kg/hectare)"),
            #set the color of the maximum as orange
            color=alt.condition(
                alt.datum.variety == my_max, 
                alt.value('red'),     
                alt.value('grey')),
            tooltip=['site', 'yield', 'variety']
            ).properties(width = 230, height=230)

            #add this chart to the list that contains all the charts
            my_graphs.append(chart)
    
    #change the way all the charts will be displayed regarding to the number of charts
    if len(my_graphs) == 1:
        my_chart = my_graphs[0]
        my_chart = my_chart.configure_title(fontSize=18
        ).configure_axis(   
        labelFontSize=14, 
        titleFontSize=18
        ).configure_title(fontSize=25)
    elif len(my_graphs) == 2:
        my_chart = alt.hconcat(my_graphs[0], my_graphs[1]).configure_title(fontSize=18
        ).configure_axis(
        labelFontSize=14, 
        titleFontSize=18
        )
    elif len(my_graphs) == 3:
        my_chart = alt.hconcat(my_graphs[0], my_graphs[1], my_graphs[2]).configure_title(fontSize=18
        ).configure_axis(
        labelFontSize=14, 
        titleFontSize=18
        )
    elif len(my_graphs) == 4:
        my_chart = alt.vconcat(alt.hconcat(my_graphs[0], my_graphs[1]), 
                              alt.hconcat(my_graphs[2], my_graphs[3])
        ).configure_title(fontSize=18
        ).configure_axis(
        labelFontSize=14, 
        titleFontSize=18
        )
    elif len(my_graphs) == 5:
        my_chart = alt.vconcat(alt.hconcat(my_graphs[0], my_graphs[1], my_graphs[2]), 
                              alt.hconcat(my_graphs[3], my_graphs[4])
        ).configure_title(fontSize=18
        ).configure_axis(
        labelFontSize=14, 
        titleFontSize=18
        )
    elif len(my_graphs) == 6:
        my_chart = alt.vconcat(alt.hconcat(my_graphs[0], my_graphs[1], my_graphs[2]), 
                              alt.hconcat(my_graphs[3], my_graphs[4], my_graphs[5])
        ).configure_title(fontSize=18
        ).configure_axis(
        labelFontSize=14, 
        titleFontSize=18
        )
    else : 
        my_chart = alt.Chart(df_temp).mark_bar()

    return my_chart.to_html()


_layout = html.Div([_sidebar_left,_body])

app.layout = _layout

if __name__ == "__main__":
    app.run_server(debug=True)