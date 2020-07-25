import json
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output

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

# load data
# todo: optimize loading data
# def load_data():
#     bucket_name
#     folder_name

with open(data + r'geojson/gadm36_IND_2_id.json', 'r') as f:
    districts_geojson = json.load(f)
df_gw_dis_mont = pd.read_parquet(data + r'gw-district-monthly.parquet.gzip')
with open(data + r'geojson/gadm36_IND_1_id.json', 'r') as f:
    states_geojson = json.load(f)
df_gw_state_mont = pd.read_parquet(data + r'gw-state-monthly.parquet.gzip')

# components viz
# main map


# ui components
resolution_main_dropdown = dcc.Dropdown(
    id='resolution-main-map',
    options=[
        {'label': 'States & UT', 'value': 'states'},
        {'label': 'Districts', 'value': 'districts'},
    ], value='states'
)
main_map_slider = dcc.Slider(
    id='slider-main-map',
    # max=list(df_gw_dis_mont.columns)[:-2][-1],
    max=len(list(df_gw_dis_mont.columns)[:-2]) - 1,
    min=0,
    value=0,
    marks={str(i): str(list(df_gw_dis_mont.columns)[i]) for i in range(len(list(df_gw_dis_mont.columns)[:-2]))},
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
main_map_card = dbc.Card(
    [
        dbc.CardHeader(resolution_main_dropdown),
        dbc.CardBody(
            [
                html.H4("Map", className="card-title"),
                dcc.Graph(id='main-map')
            ]
        ),
        dbc.CardFooter(main_map_slider)
    ]
)


def main_details_card(type_v):
    return (dbc.Card(
        dbc.CardBody(
            id=type_v
        )
    ))


# ui main

app.layout = html.Div(
    children=[
        dbc.Row(dbc.Col(navbar)),
        dbc.Row(
            [
                dbc.Col(
                    main_map_card,
                    width={"size": 10},
                ),
                dbc.Col(
                    [
                        main_details_card('region-card'),
                        main_details_card('current-card'),
                        main_details_card('prediction-card'),

                    ], width={"size": 2}
                )
            ]
        ),
    ]
)


# computation functions

# callbacks
@app.callback(
    [
        Output(component_id='region-card', component_property='children'),
        Output(component_id='current-card', component_property='children'),
        Output(component_id='prediction-card', component_property='children'),
    ],
    [Input('main-map', 'hoverData')]
)
def update_stats_callback(hover_data):
    if hover_data:
        val = hover_data['points'][0]
        return (
            ([
                html.H4(val['z'], className='card-title'),
                html.P('Current Level', className='card-text'),
            ]), ([
                html.H4(val['location'], className='card-title'),
                html.P('Location', className='card-text'),
            ]), ([
                html.H4(val['z'], className='card-title'),
                html.P('Prediction', className='card-text'),
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
                html.H4('stat', className='card-title'),
                html.P('text', className='card-text'),
            ])
        )


@app.callback(
    Output(component_id='main-map', component_property='figure'),
    [Input('resolution-main-map', 'value'),
     Input('slider-main-map', 'value')]
)
# todo: insert progress bar to update from state to district
def update_main_map(resolution_level, slider_value):
    print(slider_value, resolution_level)
    if resolution_level == 'districts':
        geojson_file = districts_geojson
        df_gw = df_gw_dis_mont
    else:
        geojson_file = states_geojson
        df_gw = df_gw_state_mont
    fig_map = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson_file,
            locations=df_gw.index.astype(str),
            z=df_gw['2020-06'].astype(float),
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


# display

# todo fix app.yaml with threads and processes
if __name__ == "__main__":
    app.run_server(debug=True)
