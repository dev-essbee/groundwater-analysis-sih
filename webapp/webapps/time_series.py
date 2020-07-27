import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from data_global_var import df_gw_pre_post, india_geojson, states_geojson, districts_geojson, blocks_geojson, \
    NO_OF_YEARS, YEARS, YEARS_PRE, YEARS_POST, YEARS_STATIONS