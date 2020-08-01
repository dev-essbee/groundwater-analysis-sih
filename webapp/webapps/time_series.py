import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from webapp import app
from data_global_var import df_gw_pre_post, india_geojson, states_geojson, districts_geojson, blocks_geojson, \
    NO_OF_YEARS, YEARS, YEARS_PRE, YEARS_POST, locations, block_cat_geojson
from webapps.home import search_bar, main_map, update_main_map_metrics_location
from dash.exceptions import PreventUpdate


#######################################################################################################################
############################################ ui components ############################################################
#######################################################################################################################

######################################### primary components ##########################################################
def min_location_graph(location, time_value):
    col_reqd = list(map(lambda year: year + '-' + time_value, YEARS))
    col_reqd = {**{i: ['mean'] for i in col_reqd}}
    geojson_file, loc, z_val, years_measured = update_main_map_metrics_location(df_gw_pre_post, col_reqd, location)
    return main_map(geojson_file, loc, z_val, years_measured, True)


time_min_map_dropdown = dcc.Dropdown(
    id='time-min-map-dropdown',
    options=[
        {'label': 'Pre-Monsoon', 'value': 'pem'},
        {'label': 'Post-Monsoon', 'value': 'pom'},
    ], value='pem'
)

########################################## Secondary Components #######################################################
min_location_card = dbc.Card(
    dbc.CardBody(
        id='location-details-card'
    )
)

#######################################################################################################################
########################################### main ui layout ############################################################
#######################################################################################################################
layout = html.Div(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    search_bar
                                ),
                                dbc.Col(
                                    time_min_map_dropdown
                                ),
                            ]
                        )
                    ], width={"size": 9}

                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        min_location_card
                                    ]
                                )
                            ]
                        )
                    ], width={"size": 3}
                )
            ]
        ),
    ]
)


#######################################################################################################################
################################################# callbacks ###########################################################
#######################################################################################################################

############################################### search bar callback ###################################################
@app.callback(
    [
        Output(component_id='location-details-card', component_property='children'),
    ],
    [Input('search-bar', 'value'),
     Input('time-min-map-dropdown', 'value')
     ]
)
def update_min_locations_callback(location_value, time_value):
    print(location_value, time_value)
    if not location_value:
        location_value = 'India : india'
        return (
            ([
                dcc.Graph(id='location-min-graph', figure=min_location_graph(location_value, time_value)),
                # html.H4(location_value, className='card-title'),
                # html.P('some text', className='card-text'),
                # html.H4('stat', className='card-title'),
                # html.P('text', className='card-text'),

            ])
        )
    else:
        if location_value in locations:
            return (
                ([
                    dcc.Graph(id='location-min-graph', figure=min_location_graph(location_value, time_value)),
                    # html.H4(location_value, className='card-title'),
                    # html.P('some text', className='card-text'),
                    # html.H4('stat', className='card-title'),
                    # html.P('text', className='card-text'),

                ])
            )
        else:
            raise PreventUpdate
