import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import gcsfs
from webapp import app
from data_global_var import df_gw_pre_post, india_geojson, states_geojson, districts_geojson, blocks_geojson, \
    NO_OF_YEARS, YEARS, YEARS_PRE, YEARS_POST, YEARS_STATIONS, locations
from dash.exceptions import PreventUpdate


# import os, sys
# dir_path = os.path.dirname(os.path.realpath(__file__))
# parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
# sys.path.insert(0, parent_dir_path)
# import data_import
# location variables


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


def years_measured_plot(value):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=int(value),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Years Measured"},
        gauge={'axis': {'range': [None, NO_OF_YEARS], 'tickwidth': 1, 'tickcolor': "darkblue"},
               'bar': {'color': "RebeccaPurple"},
               'bgcolor': "white",
               'borderwidth': 2,
               'bordercolor': "gray"}))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, transition_duration=500)
    return fig


def main_map(geojson_file, loc, z_val, years_measured):
    fig_map = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_file,
            locations=loc,
            z=z_val,
            customdata=years_measured,
            colorscale="Bluered",
            zmin=0,
            zmax=12,
            marker_opacity=0.5,
            marker_line_width=0,
            colorbar=dict(thickness=15, ticklen=3),
        )
    )
    fig_map.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3.25,
        mapbox_center={"lat": 22.775, "lon": 75.8577},
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
# main_map_slider = dcc.Slider(
#     id='slider-main-map',
#     max=NO_OF_YEARS,
#     min=0,
#     value=0,
#     marks={
#         str(i): str(int(list(df_gw_pre_post.columns)[4].split('-')[0]) + i)
#         for i in range(0, NO_OF_YEARS)
#     },
#     step=None
# )
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink('Time Series Analysis', href="/time-series")
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


def get_search_datalist_option(locs):
    options = []
    for loc in locs:
        options.append(html.Option(value=loc))
    # print(options[:5])
    return options


search_bar = [html.Datalist(id='search-bar-datalist', children=get_search_datalist_option(locations)),
              dbc.Input(id='search-bar', placeholder='Type to search a place', type='search', autoComplete=True,
                        list='search-bar-datalist')]

########################################## Secondary Components #######################################################

main_map_card = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Row(
                [
                    dbc.Col(resolution_main_dropdown),
                    dbc.Col(time_main_dropdown),
                    dbc.Col(search_bar)

                ]
            )
        ),
        dbc.CardBody(
            [
                html.H4("Map", className="card-title"),
                dcc.Graph(id='main-map')
            ]
        ),
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
layout = html.Div(
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

############################################### search bar callback ###################################################
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
                dcc.Graph(id='years-measured-graph', figure=years_measured_plot(val['customdata'])),
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
                dcc.Graph(id='years-measured-graph', figure=years_measured_plot(NO_OF_YEARS)),
            ])
        )


@app.callback(
    Output(component_id='main-map', component_property='figure'),
    [Input('resolution-main-map', 'value'),
     Input('time-main-map', 'value'),
     Input('search-bar', 'value')]
)
# todo: insert progress bar to update from state to district
def update_main_map(resolution_level, time_value, location):
    # print('start', resolution_level, slider_value, time_value)
    # print(0, location)
    col_reqd = list(map(lambda year: year + '-' + time_value, YEARS))
    col_reqd = {**{i: ['mean'] for i in col_reqd}, **{'total-stations': ['sum']}}

    if not location:
        # print(1, location)
        geojson_file, loc, z_val, years_measured = update_main_map_metrics(resolution_level, df_gw_pre_post, col_reqd)
        return main_map(geojson_file, loc, z_val, years_measured)
    else:
        if location in locations:
            geojson_file, loc, z_val, years_measured = update_main_map_metrics_location(df_gw_pre_post,
                                                                                       col_reqd,
                                                                                       location)
            # todo disable dropdown on location search
            # todo update metrics too on search
            return main_map(geojson_file, loc, z_val, years_measured)
        else:
            # print(2, location)
            raise PreventUpdate


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


# todo fix app.yaml with threads and processes
############################################# Utility functions ######################################################
def update_main_map_metrics(resolution_level, df_gw_pre_post, clmns_reqd):
    # print(df_gw)
    df_gw = df_gw_pre_post.groupby(resolution_level).agg(
        clmns_reqd).round(2)
    df_gw = df_gw.loc[:, (clmns_reqd, 'mean')]
    years_measured=df_gw.notna().sum(axis=1)
    df_gw = df_gw.mean(axis=1).round(2)
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
    return geojson_file, loc, z_val, years_measured


def update_main_map_metrics_location(df_gw_pre_post, clmns_reqd, location):
    location = location.split(':')
    # print('up', location)
    res = location[1].lower().strip()
    location = location[0].strip()
    location = location.lower()
    # print(1, location, res)
    # print(df_gw)
    df_gw = df_gw_pre_post.groupby(res).agg(
        clmns_reqd).round(2)
    df_gw = df_gw.loc[location, (clmns_reqd, 'mean')]
    years_measured=[df_gw.notna().sum()]
    df_gw=df_gw.mean().round(2)
    z_val = [df_gw]
    loc = [location]
    if res == 'india':
        geojson_file = india_geojson
    elif res == 'state':
        geojson_file = states_geojson
    elif res == 'district':
        geojson_file = districts_geojson
    else:
        geojson_file = blocks_geojson
    # print(type(fig_map))
    return geojson_file, loc, z_val, years_measured
