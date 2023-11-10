from dash import html, dcc, callback, Output, Input, State, ALL  # Include State and ALL here
from rdflib import Graph
from app import app

# Assume you have a Graph loaded with your .ttl file
g = Graph()
g.parse("final.ttl", format="ttl")

# Initialize the current level URI with the main system URI
current_level_uri = 'http://10.63.126.170:31886/things/B43'

layout = html.Div([
    dcc.Textarea(id='sparql-query', 
    value='PREFIX ssn: <http://www.w3.org/ns/ssn/> SELECT ?subSystem WHERE { <http://10.63.126.170:31886/things/B43> ssn:hasSubSystem ?subSystem . }', style={'width': '100%', 'height': '200px'}),
    html.Button('Run Query', id='run-query-btn'),
    html.Button('Go Back', id='go-back-btn'),
    html.Pre(id='query-output'),
    dcc.Store(id='current-level-uri', data=current_level_uri)  # Store the current level URI
])

@app.callback(
    Output('query-output', 'children'),
    [Input('run-query-btn', 'n_clicks')],
    [State('sparql-query', 'value')]
)
def execute_query(n_clicks, query):
    if n_clicks:
        try:
            # Execute SPARQL query
            result = g.query(query)
            # Format the result as desired
            csv_str = result.serialize(format='csv')
            return csv_str.decode('utf-8')
        except Exception as e:
            return f'An error occurred: {e}'
    return ''

@app.callback(
    Output('current-level-uri', 'data'),  # Update the current level URI in the Store
    [Input('go-back-btn', 'n_clicks')],
    [State('current-level-uri', 'data')]
)
def go_back(n_clicks, current_uri):
    if n_clicks:
        # Split the current URI by '/' to go back one level
        uri_parts = current_uri.split('/')
        if len(uri_parts) > 1:
            new_uri = '/'.join(uri_parts[:-1])
            return new_uri
    return current_uri

# Update the query based on the current level URI
@app.callback(
    Output('sparql-query', 'value'),
    [Input('current-level-uri', 'data')]
)
def update_query(current_uri):
    return f'PREFIX ssn: <http://www.w3.org/ns/ssn/> SELECT ?subSystem WHERE {{ <{current_uri}> ssn:hasSubSystem ?subSystem . }}'

if __name__ == '__main__':
    app.run_server(debug=True)
