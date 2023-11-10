from dash import Dash, html, dcc, Output, Input, State, ALL, callback_context
import dash
import json
from rdflib import Graph, URIRef
from snowflake_connection import SnowflakeConnector
from rdf_to_snowflake import SparqlRunner

# Initialize and load your RDF graph
g = Graph()
g.parse("final.ttl", format="ttl")

# The main system URI
main_system_uri = 'http://10.63.126.170:31886/things/B43'

# Keep track of the current level URI
current_level_uri = main_system_uri

# Function to query and return the hierarchy
def query_hierarchy(entity_uri):
    query = """
    PREFIX ssn: <http://www.w3.org/ns/ssn/>
    ASK { <%s> ssn:hasSubSystem ?subsystem } limit 10000
    """ % entity_uri
    has_subsystems = g.query(query).askAnswer
    
    if has_subsystems:
        query = """
        SELECT ?subsystem WHERE {
          <%s> ssn:hasSubSystem ?subsystem .
        } limit 10000
        """ % entity_uri
        subsystems = g.query(query)
        return html.Ul([html.Li(html.Button(str(subsystem['subsystem'].split('/')[-1]), id={'type': 'dynamic-button', 'index': str(subsystem['subsystem'])}, n_clicks=0)) for subsystem in subsystems])
    else:
        query = """
        SELECT ?property ?value WHERE {
          <%s> ?property ?value .
        } limit 10000
        """ % entity_uri
        properties = g.query(query)
        property_dict = {
            f"value_{index}": f"{entity_uri}{prop['value'].split('/')[-1]}"
            for index, prop in enumerate(properties)
        }
        serialized_property_dict = json.dumps(property_dict)
        property_elements = [
            html.Li([
                dcc.Checklist(
                    options=[{'label': '', 'value': 'selected'}],
                    id={'type': 'property-checkbox', 'index': index},
                    value=[],
                    inputStyle={"margin-right": "5px"}
                ),
                f" {value}",
                html.Span('', id={'type': 'success-text', 'index': index})
            ])
            for index, value in property_dict.items()
        ]
        return html.Div([
            html.Ul(property_elements),
            dcc.Store(id='property-dict-store', data=serialized_property_dict)
        ])

# Define the predefined function
def my_predefined_function(property_value):
    proto = SparqlRunner()
    return proto.plot_results(property_value)

# Layout for the page
layout = html.Div([
    html.Button('B43', id='main-system', n_clicks=0),
    html.Button('Back', id='back-button', n_clicks=0),
    html.Div(id='system-hierarchy'),
    dcc.Store(id='property-dict-store')
])

# Callback to handle clicks and update display
@dash.callback(
    Output('system-hierarchy', 'children'),
    [Input('main-system', 'n_clicks'), Input('back-button', 'n_clicks'), Input({'type': 'dynamic-button', 'index': ALL}, 'n_clicks')],
    [State('system-hierarchy', 'children')],
    prevent_initial_call=True
)
def display_hierarchy(main_click, back_click, subsystem_clicks, current_display):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update

    triggered_id = ctx.triggered[0]['prop_id']
    global current_level_uri

    if 'main-system' in triggered_id:
        current_level_uri = main_system_uri
        return query_hierarchy(main_system_uri)
    elif 'back-button' in triggered_id and current_display:
        # Logic to go back to the previous level
        pass
    else:
        entity_uri = triggered_id.split('"index":"')[1].split('",')[0]
        current_level_uri = entity_uri
        return query_hierarchy(entity_uri)

    return html.Div()

# Callback to update the success text
@dash.callback(
    Output({'type': 'success-text', 'index': ALL}, 'children'),
    Input({'type': 'property-checkbox', 'index': ALL}, 'value'),
    State('property-dict-store', 'data'),
    prevent_initial_call=True
)
def update_success_text(checkbox_values, serialized_property_dict):
    property_dict = json.loads(serialized_property_dict) if serialized_property_dict else {}
    response = []
    for i, value in enumerate(checkbox_values):
        if 'selected' in value:
            property_value = property_dict.get(f'value_{i}')
            if property_value:
                response.append(my_predefined_function(property_value))
            else:
                response.append('')
        else:
            response.append('')
    return response
