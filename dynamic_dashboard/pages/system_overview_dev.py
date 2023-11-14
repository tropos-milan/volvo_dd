from dash import Dash, html, dcc, Output, Input, State, ALL, callback_context
import json
from rdflib import Graph, URIRef
from snowflake_connection import SnowflakeConnector
from rdf_to_snowflake import SparqlRunner
from app import app
import re

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
    ASK { <%s> ssn:hasSubSystem ?subsystem } 
    """ % entity_uri
    has_subsystems = g.query(query).askAnswer
    
    if has_subsystems:
        query = """
        SELECT ?subsystem WHERE {
          <%s> ssn:hasSubSystem ?subsystem .
        } 
        """ % entity_uri
        subsystems = g.query(query)
        return html.Ul([html.Li(html.Button(str(subsystem['subsystem'].split('/')[-1]), id={'type': 'dynamic-button', 'index': str(subsystem['subsystem'])}, n_clicks=0)) for subsystem in subsystems])
    else:
        query = """
        SELECT ?property ?value WHERE {
          <%s> ?property ?value .
        } 
        """ % entity_uri
        properties = g.query(query)
        property_dict = {
            f"value_{index}": f"{entity_uri}{prop['value'].split('/')[-1]}"
            for index, prop in enumerate(properties)
        }
        serialized_property_dict = json.dumps(property_dict)
        property_elements = [
        html.Li([
            html.Div([
                dcc.Checklist(
                    options=[{'label': re.sub(r'^.*?([A-Z][a-zA-Z]*)$', r'\1', value.split('/')[-1]), 'value': 'selected'}],
                    id={'type': 'property-checkbox', 'index': index},
                    value=[],
                    style={"display": "inline-block", "margin-right": "5px"}
                ),
                html.Span('', id={'type': 'success-text', 'index': index})
            ], style={"display": "flex", "alignItems": "center"})
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
    dcc.Store(id='property-dict-store'),

])

