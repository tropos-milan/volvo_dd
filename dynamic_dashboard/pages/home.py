# Import necessary Dash components
from dash import html, dcc

# Define the layout for the home page
layout = html.Div([
    html.H1("Welcome to the dynamic dashboard"),
    html.P("Navigate to a page:"),
    html.Div([dcc.Link('Go to System Overview', href='/system-overview')]),
    html.Div([dcc.Link('Query the RDF database', href='/query-page')]),
    html.Div([dcc.Link('Dashboard', href='/system-overview-dev')]),
    # Add more divs as needed for other pages
    # html.Div([dcc.Link('Go to About Page', href='/about')]),
])
