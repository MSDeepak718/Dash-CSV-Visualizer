from dash import html, dcc, dash_table, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import base64
import io
from flask import session
from dash.exceptions import PreventUpdate
import polars as pl

def read_csv_safely(file_path):
    encodings = ["utf-8", "latin1", "ISO-8859-1", "utf-8-sig"]
    delimiters = [",", ";", "\t"]

    for encoding in encodings:
        for delimiter in delimiters:
            try:
                df = pl.read_csv(file_path, encoding=encoding, separator=delimiter)
                if len(df.columns) > 1:
                    return df
            except Exception:
                continue

    raise ValueError("Failed to read the CSV file with common encodings and delimiters.")


try:
    default_df = read_csv_safely('Superstore.csv')
except Exception as e:
    default_df = pl.DataFrame()
    print(f"Error loading default CSV: {e}")

layout = html.Div(id="protected-content")

@callback(
    Output("protected-content", "children"),
    Input("url", "pathname"),
    prevent_initial_call=False
)
def protected_layout(pathname):
    if not session.get("logged_in"):
        return dcc.Location(href="/login", id="redirect-login")

    return dbc.Container([
        html.H1("CSV Data Visualizer", className="text-center mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Button("Logout", id="logout-button", color="danger", className="float-end"),
            ], width=12),
        ], className="mb-3"),

        html.Hr(),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Upload & Controls", className="card-title text-center mb-3"),

                        dcc.Upload(
                            id='upload-data',
                            children=dbc.Button("Upload CSV", color="primary", className="w-100"),
                            multiple=False,
                            style={"textAlign": "center", "marginBottom": "15px"}
                        ),

                        html.Label("X-Axis:", className="fw-bold"),
                        dcc.Dropdown(id='dropdown-x-axis', className='mb-3'),

                        html.Label("Y-Axis:", className="fw-bold"),
                        dcc.Dropdown(id='dropdown-y-axis', className='mb-3'),

                        dbc.RadioItems(
                            options=[
                                {"label": "Graph", "value": "graph"},
                                {"label": "Table", "value": "table"},
                            ],
                            value="table",
                            id="toggle-view",
                            inline=True,
                            className="d-flex justify-content-center mt-2"
                        ),
                    ])
                ], className="shadow-lg p-3 mb-2 bg-white rounded"),
            ], md=4),

            dbc.Col(html.Div(id="content-container"), md=8),
        ]),
    ], fluid=True)

def parse_uploaded_file(contents):
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pl.read_csv(io.BytesIO(decoded))
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return default_df

@callback(
    [Output('dropdown-x-axis', 'options'),
     Output('dropdown-y-axis', 'options'),
     Output('dropdown-x-axis', 'value'),
     Output('dropdown-y-axis', 'value')],
    Input('upload-data', 'contents')
)
def update_dropdowns(contents):
    df = parse_uploaded_file(contents) if contents else default_df
    
    numeric_columns = [col for col in df.columns if df[col].dtype in [pl.Int32, pl.Int64, pl.Float32, pl.Float64]]

    if len(numeric_columns) < 2:
        return [], [], None, None

    return numeric_columns, numeric_columns, numeric_columns[0], numeric_columns[1]


@callback(
    Output('content-container', 'children'),
    Input('toggle-view', 'value'),
    Input('dropdown-x-axis', 'value'),
    Input('dropdown-y-axis', 'value'),
    State('upload-data', 'contents')
)
def update_content(view, x_axis, y_axis, contents):
    if not session.get("logged_in"):
        raise PreventUpdate

    df = parse_uploaded_file(contents) if contents else default_df

    if view == "graph":
        return dcc.Graph(figure=px.line(df, x=x_axis, y=y_axis))

    return dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.head(100).to_dicts(),

        style_table={
            "maxHeight": "400px",
            "overflowY": "auto",
            "borderRadius": "10px",
            "boxShadow": "0px 0px 10px rgba(0, 0, 0, 0.1)",
        },

        style_cell={
            "textAlign": "center",
            "padding": "10px",
            "fontSize": "14px",
            "fontFamily": "Arial, sans-serif",
        },

        style_header={
            "backgroundColor": "#007bff",
            "color": "white",
            "fontWeight": "bold",
            "border": "1px solid white",
        },

        style_data={
            "backgroundColor": "#f8f9fa",
            "border": "1px solid #dee2e6",
        },

        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#e9ecef"},
            {"if": {"state": "active"}, "backgroundColor": "#d1ecf1", "color": "black", "fontWeight": "bold"},
        ],

        style_as_list_view=True,

        page_size=50,
        page_action="native",
        sort_action="native",
    )

@callback(
    Output("url", "pathname"),
    Input("logout-button", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    session.pop("logged_in", None)
    return "/login"
