import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from webapp import app
from webapps import home, time_series

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/time-series':
        return time_series.layout
    else:
        return '404'


#######################################################################################################################
################################################ run ##################################################################
#######################################################################################################################
if __name__ == '__main__':
    app.run_server(debug=True)
