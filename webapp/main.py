import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
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
])
app.title = 'Analysis GroundWater India'
# components viz
fig_map=go.Figure(
    data=go.Choropleth(
        locations=["India"]
    )
)
# fig_map.add_trace()
# fig_map.update_layout()

# ui
app.layout = html.Div(
    children=[
        # Heading of the webapp
        html.H3(children='Groundwater Analysis and Management for India'),
        # Map
        dcc.Graph(
            id='main-map',
            figure=fig_map
        )
    ]

)

# computation functions


# display
if __name__ == "__main__":
    app.run_server(debug=True)
