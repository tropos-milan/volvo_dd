from dash import Dash, html, dcc, Output, Input, State, ALL, callback_context

import json
from app import app
from pages.system_overview_dev import query_hierarchy, my_predefined_function

main_system_uri = 'http://10.63.126.170:31886/things/B43'
# Modified Callback to handle clicks and update display
@app.callback(
    Output('system-hierarchy', 'children'),
    [Input('main-system', 'n_clicks'), Input('back-button', 'n_clicks'), Input({'type': 'dynamic-button', 'index': ALL}, 'n_clicks')],
    [State('system-hierarchy', 'children')],
    prevent_initial_call=True
)
def display_hierarchy(main_click, back_click, subsystem_clicks, current_display):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update

    global current_level_uri
    global navigation_history

    triggered_id = ctx.triggered[0]['prop_id']

    if 'main-system' in triggered_id:
        current_level_uri = main_system_uri
        navigation_history = [main_system_uri]  # Reset history
        return query_hierarchy(main_system_uri)
    elif 'back-button' in triggered_id and len(navigation_history) > 1:
        navigation_history.pop()  # Remove the current level
        current_level_uri = navigation_history[-1]  # Get the previous level
        return query_hierarchy(current_level_uri)
    else:
        entity_uri = triggered_id.split('"index":"')[1].split('",')[0]
        current_level_uri = entity_uri
        if current_level_uri not in navigation_history:
            navigation_history.append(current_level_uri)  # Add to history
        return query_hierarchy(entity_uri)

    return html.Div()


@app.callback(
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