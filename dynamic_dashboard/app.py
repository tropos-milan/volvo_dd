# app.py
from dash import Dash

app = Dash(__name__, suppress_callback_exceptions=True)

# This line is necessary if you're using CSS/JS in the assets directory
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

if __name__ == '__main__':
    app.run_server(debug=True)

