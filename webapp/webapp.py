import json
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import gcsfs
# import os, sys
# dir_path = os.path.dirname(os.path.realpath(__file__))
# parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
# sys.path.insert(0, parent_dir_path)
# import data_import
# location variables
data = r"../data/"

# initial set up of the app
app = dash.Dash(__name__, meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'description',
        'content': 'My description'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1.0'
    }
], external_stylesheets=[dbc.themes.MATERIA])
app.title = 'Analysis GroundWater India'
#######################################################################################################################
################################################### load data #########################################################
#######################################################################################################################
# todo: optimize loading data
# def load_data():
#     bucket_name
#     folder_name

df_gw_pre_post = pd.read_parquet(data + r'comp/gw-block-pre-post.parquet.gzip')
with open(data + r'geojson/gadm36_IND_0_id.json', 'r') as f:
    india_geojson = json.load(f)
with open(data + r'geojson/gadm36_IND_1_id.json', 'r') as f:
    states_geojson = json.load(f)
with open(data + r'geojson/gadm36_IND_2_id.json', 'r') as f:
    districts_geojson = json.load(f)
with open(data + r'geojson/gadm36_IND_3_id.json', 'r') as f:
    blocks_geojson = json.load(f)
# important constants
NO_OF_YEARS = (len(list(df_gw_pre_post.columns)) - 4) // 3
YEARS = [str(i + 1994) for i in range(NO_OF_YEARS)]
YEARS_PRE = list(map(lambda year: year + "-pre", YEARS))
YEARS_POST = list(map(lambda year: year + "-post", YEARS))
YEARS_STATIONS = list(map(lambda year: year + "-stations", YEARS))
YEARS_STATIONS.append("total-stations")


#######################################################################################################################
############################################ visualizations ###########################################################
#######################################################################################################################
def trend_scatter_plot(df_gw):
    fig = go.Figure(data=go.Scatter(x=YEARS, y=df_gw.values))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, transition_duration=500)
    return fig


def stations_bar_graph(stations_per):
    fig_stations = go.Figure([go.Bar(x=YEARS, y=stations_per)])
    fig_stations.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, transition_duration=500)
    return fig_stations


def no_stations_plot(value):
    print(value)
    used = value.split('/')
    total = int(used[1])
    used = int(used[0])
    # print(total, used, value)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=int((used / total) * 100),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Stations Measured"},
        gauge={'axis': {'range': [None, 100]}}
    ))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, transition_duration=500)
    return fig


def main_map(geojson_file, loc, z_val, stations_info):
    fig_map = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_file,
            locations=loc,
            z=z_val,
            customdata=stations_info,
            colorscale="Viridis",
            zmin=0,
            zmax=12,
            marker_opacity=0.5,
            marker_line_width=0,
        )
    )
    fig_map.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3,
        mapbox_center={"lat": 26.9124, "lon": 75.7873},
    )
    fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, transition_duration=500)
    return fig_map


#######################################################################################################################
############################################ ui components ############################################################
#######################################################################################################################

######################################### primary components ##########################################################

resolution_main_dropdown = dcc.Dropdown(
    id='resolution-main-map',
    options=[
        {'label': 'India', 'value': 'india'},
        {'label': 'States & UT', 'value': 'state'},
        {'label': 'Districts', 'value': 'district'},
        {'label': 'Blocks', 'value': 'block'},
    ], value='india'
)
time_main_dropdown = dcc.Dropdown(
    id='time-main-map',
    options=[
        {'label': 'Pre-Monsoon', 'value': 'pre'},
        {'label': 'Post-Monsoon', 'value': 'post'},
    ], value='pre'
)
main_map_slider = dcc.Slider(
    id='slider-main-map',
    max=NO_OF_YEARS,
    min=0,
    value=0,
    marks={
        str(i): str(int(list(df_gw_pre_post.columns)[4].split('-')[0]) + i)
        for i in range(0, NO_OF_YEARS)
    },
    step=None
)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink('Something', href="#")
        ),
        dbc.NavItem(
            dbc.NavLink('Something', href="#")
        )
    ],
    brand='Webapp name',
    brand_href='#',
    color='primary',
    dark=True,
)

########################################## Secondary Components #######################################################

main_map_card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(resolution_main_dropdown),
                    dbc.Col(time_main_dropdown)
                ]
            )
        ),
        dbc.CardBody(
            [
                html.H4("Map", className="card-title"),
                dcc.Graph(id='main-map')
            ]
        ),
        dbc.CardFooter(main_map_slider)
    ]
)

trend_graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Trend", className="card-title"),
            dcc.Graph(id='trend-graph')
        ]
    )
)

trend_stations_card = dbc.Card(
    [
        html.H4("Stations Measured", className="card-title"),
        dcc.Graph(id='trend-stations-graph')
    ]
)


def main_details_card(type_v):
    return (dbc.Card(
        dbc.CardBody(
            id=type_v
        )
    ))


#######################################################################################################################
########################################### main ui layout ############################################################
#######################################################################################################################
app.layout = html.Div(
    children=[
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(
            [
                dbc.Col(
                    main_map_card,
                    width={"size": 9},
                ),
                dbc.Col(
                    [
                        main_details_card('region-card'),
                        main_details_card('current-card'),
                        main_details_card('no-stations-card'),

                    ], width={"size": 3}
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    trend_graph_card,
                    width={"size": 6},
                ),
                dbc.Col(
                    trend_stations_card,
                    width={'size': 6},
                )
            ]
        )
    ]
)


# computation functions
#######################################################################################################################
################################################# callbacks ###########################################################
#######################################################################################################################

################################################# Main Trend Callback ##################################################


@app.callback(
    [Output('trend-graph', 'figure'),
     Output('trend-stations-graph', 'figure')
     ],
    [Input('resolution-main-map', 'value'),
     Input('main-map', 'clickData'),
     Input('time-main-map', 'value')]
)
def update_trend_callback(resolution, click_data, time):
    hover_value = 'india'
    if not click_data:
        if resolution == 'state':
            hover_value = 'rajasthan'
        elif resolution == 'district':
            hover_value = 'jaipur'
        elif resolution == 'block':
            hover_value = 'amber'
    else:
        hover_value = click_data['points'][0]['location']
    if time == 'pre':
        temp_years = YEARS_PRE
    else:
        temp_years = YEARS_POST
    df = (
        df_gw_pre_post.iloc[list(df_gw_pre_post[df_gw_pre_post[resolution] == hover_value].index)].agg(
            {
                **{i: ["mean"] for i in temp_years},
                **{i: ["sum"] for i in YEARS_STATIONS},
            }
        ).round(2)
    )
    df_gw = df.loc['mean', temp_years]
    # print(YEARS, df.values, df)

    # print(hover_value)
    fig = trend_scatter_plot(df_gw)
    df_stations = df.loc['sum', YEARS_STATIONS[:-1]]
    stations_per = (df_stations / df.loc['sum', YEARS_STATIONS[-1]]) * 100
    # print(stations_per)
    fig_stations = stations_bar_graph(stations_per)
    return fig, fig_stations


############################################## Main Info Callback #####################################################
@app.callback(
    [
        Output(component_id='region-card', component_property='children'),
        Output(component_id='current-card', component_property='children'),
        Output(component_id='no-stations-card', component_property='children'),
    ],
    [Input('main-map', 'hoverData')]
)
def update_stats_callback(hover_data):
    if hover_data:
        val = hover_data['points'][0]
        # print(hover_data)
        return (
            ([
                html.H4(val['z'], className='card-title'),
                html.P('Current Level', className='card-text'),
            ]), ([
                html.H4(val['location'], className='card-title'),
                html.P('Location', className='card-text'),
            ]), ([
                dcc.Graph(id='no-stations-graph', figure=no_stations_plot(val['customdata'])),
            ])
        )
    else:
        return (
            ([
                html.H4('stat', className='card-title'),
                html.P('text', className='card-text'),
            ]), ([
                html.H4('stat', className='card-title'),
                html.P('text', className='card-text'),
            ]), ([
                dcc.Graph(id='no-stations-graph', figure=no_stations_plot('1/1')),
            ])
        )


@app.callback(
    Output(component_id='main-map', component_property='figure'),
    [Input('resolution-main-map', 'value'),
     Input('slider-main-map', 'value'),
     Input('time-main-map', 'value')]
)
# todo: insert progress bar to update from state to district
def update_main_map(resolution_level, slider_value, time_value):
    # print('start', resolution_level, slider_value, time_value)
    year = str(int(slider_value) + 1994)
    col_reqd = year + '-' + str(time_value)
    df_gw = df_gw_pre_post.groupby(resolution_level).agg(
        {col_reqd: ['mean'], year + '-stations': ['sum'], 'total-stations': ['sum']}).round(2)
    # print(df_gw)
    used_stations = list(map(int, df_gw.loc[:, (year + '-stations', 'sum')]))
    total_stations = list(map(int, df_gw.loc[:, ('total-stations', 'sum')]))
    stations_info = [str(used_stations[i]) + '/' + str(total_stations[i]) for i in range(len(used_stations))]
    df_gw = df_gw.loc[:,
            (year + '-' + str(time_value), 'mean')]
    z_val = df_gw.tolist()
    loc = df_gw.index.tolist()
    if resolution_level == 'india':
        geojson_file = india_geojson
    elif resolution_level == 'state':
        geojson_file = states_geojson
    elif resolution_level == 'district':
        geojson_file = districts_geojson
    else:
        geojson_file = blocks_geojson
    # print(type(fig_map))
    return main_map(geojson_file, loc, z_val, stations_info)


#######################################################################################################################
################################################ run ##################################################################
#######################################################################################################################

# todo fix app.yaml with threads and processes
if __name__ == "__main__":
    app.run_server(debug=True)
