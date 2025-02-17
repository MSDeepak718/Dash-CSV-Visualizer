from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Welcome to the Data Visualizer", className="text-center"),
    html.Br(),
    html.P("Please log in to access the visualization tool.", className="text-center"),
    dbc.Button("Go to Login", href="/login", color="primary", className="d-block mx-auto"),
], className="vh-100 d-flex flex-column justify-content-center align-items-center")
