import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import gcsfs
from webapp import app
from data_global_var import df_gw_pre_post, india_geojson, states_geojson, districts_geojson, blocks_geojson, \
    NO_OF_YEARS, YEARS, YEARS_PRE, YEARS_POST, locations, block_cat_geojson,categories
from dash.exceptions import PreventUpdate


############################################# Utility functions ######################################################
def cat_block_map_metrics():
    loc = categories.loc[:, 'block']
    z_val = categories.loc[:,'cat_val']
    # print(loc[:10],z_val[:10])
    return cat_block_map(block_cat_geojson, loc, z_val)


#######################################################################################################################
############################################ ui components ############################################################
#######################################################################################################################

######################################### primary components ##########################################################
def cat_block_map(block_cat_geojson, loc, z_val):
    # print(z_val)
    cat_block_map = go.Figure(
        go.Choroplethmapbox(
            geojson=block_cat_geojson,
            locations=loc,
            z=z_val,
            colorscale="Bluered",
            colorbar=dict(thickness=15, ticklen=3),
        )
    )
    # fig.update_geos(fitbounds="locations", visible=False)
    cat_block_map.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=3.25,
        mapbox_center={"lat": 22.775, "lon": 75.8577},
    )
    cat_block_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, transition_duration=500)
    return cat_block_map


######################################### secondary components ########################################################
cat_block_map_card = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(figure=cat_block_map_metrics(), id='cat-block-map')
        ]
    )
)

#######################################################################################################################
########################################### main ui layout ############################################################
#######################################################################################################################
layout = html.Div(
    children=[
        dbc.Row(
            dbc.Col(html.H5('search-bar'))
        ),
        dbc.Row(
            cat_block_map_card
        )
    ]
)

#######################################################################################################################
################################################# callbacks ###########################################################
#######################################################################################################################

############################################### cat map callback ###################################################
