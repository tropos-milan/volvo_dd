# system_overview.py
from dash import html, dcc, callback, Output, Input
from rdflib import Graph

# Assume g is your initialized and loaded graph
g = Graph()
g.parse("final.ttl", format="ttl")

# Fetch all systems
query_all_systems = """
PREFIX ssn: <http://www.w3.org/ns/ssn/>
SELECT ?system WHERE {
  ?system a ssn:System .
}
"""
results = g.query(query_all_systems)

# Extract just the 'X' part from the URI
system_ids = [str(result['system'].split('/')[-1]) for result in results]

# Layout for the page
layout = html.Div([
    dcc.Checklist(
        id='system-selection',
        options=[{'label': system_id, 'value': system_id} for system_id in system_ids],
        value=[],
        labelStyle={'display': 'block'}
    ),
    html.Div(id='subsystem-display')
])

# Callback to update the subsystem display
@callback(
    Output('subsystem-display', 'children'),
    Input('system-selection', 'value')
)
def update_subsystem_display(selected_systems):
    # Here you would query for subsystems based on the selected_systems
    # and generate the content to display. This is just a placeholder.
    return html.Ul([html.Li(system) for system in selected_systems])

# Don't forget to import this page in your index.py and add it to your app layout
