from dash import Dash, html, dcc, Input, Output
from app import app
import pages.query_page  # Make sure to create this module
from pages.system_overview import layout as system_overview_layout
from pages.home import layout as home_layout
from pages.system_overview_dev import layout as layout_dev

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/home' or pathname == '/':
        return home_layout
    if pathname == '/query-page':
        return pages.query_page.layout
    elif pathname == '/system-overview':
        return system_overview_layout
    elif pathname == '/system-overview-dev':
        return layout_dev

    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
