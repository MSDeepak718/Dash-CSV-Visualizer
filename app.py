from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from flask import session, redirect
from flask_session import Session
from server import server
import config
from pages import visualize, home, login

# Initialize Dash app
app = Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

server.config.from_object(config.Config)
Session(server)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == "/visualize":
        if not session.get("logged_in"):  
            return dcc.Location(href="/login", id="redirect-login")
        return visualize.layout
    elif pathname == "/login":
        return login.layout
    return home.layout

if __name__ == "__main__":
    app.run(debug=True)
