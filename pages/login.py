from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from flask import session

layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Login", className="text-center mb-3"),
            dbc.Input(id="username", type="text", placeholder="Username", className="mb-3"),
            dbc.Input(id="password", type="password", placeholder="Password", className="mb-3"),
            dbc.Button("Login", id="login-button", color="primary", className="w-100"),
            html.Div(id="login-output", className="mt-3 text-danger text-center"),
        ], width=4, className="shadow p-4 bg-white rounded"),
    ], className="justify-content-center align-items-center vh-100 d-flex"),
], fluid=True)
USER_CREDENTIALS = {"admin": "123"}

@callback(
    Output("login-output", "children"),
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def authenticate(n_clicks, username, password):
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        session["logged_in"] = True
        return dcc.Location(href="/visualize", id="redirect")
    return "Invalid username or password"
