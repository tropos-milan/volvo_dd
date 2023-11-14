from dash import html, dcc

def serve_layout():
    return html.Div([
        # Styling the navigation bar
        html.Nav([
            dcc.Link('Home', href='/', style={
                'color': '#007BFF',  # Link color
                'textDecoration': 'none',
                'padding': '8px 16px',
                'fontWeight': 'bold'
            }),
            # Add other common navigation links if necessary
            # Remember to style them similarly
        ], style={
            'backgroundColor': '#F8F9FA',  # Background color of the navbar
            'padding': '10px',
            'boxShadow': '0 2px 4px rgba(0,0,0,.1)'
        }),
        # Styling the content container
        html.Div(id='page-content', style={
            'marginTop': '20px',  # Space between nav and content
            'marginLeft': '5%',
            'marginRight': '5%',
            'padding': '20px',
            'backgroundColor': '#FFFFFF',  # Background color of content area
            'boxShadow': '0 2px 4px rgba(0,0,0,.1)',
            'borderRadius': '5px'
        }),
        dcc.Location(id='url', refresh=False)
    ], style={
        'fontFamily': 'Arial, sans-serif',  # Global font style
        'backgroundColor': '#E9ECEF',  # Background color of the whole page
        'height': '100vh',  # Full view height
        'margin': '0'
    })
