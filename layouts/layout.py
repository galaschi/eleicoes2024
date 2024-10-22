# layouts/layout.py
import dash_bootstrap_components as dbc
from dash import dcc, html


def create_layout():
    layout = dbc.Container([
        html.H1("Resultados Eleições 2024 - Novo Hamburgo", className="text-center my-4"),

        # Toggle para selecionar o cargo (Prefeito ou Vereador)
        dbc.Row([
            dbc.Col(html.Label('Selecione o Cargo:', className="h5 font-weight-bold")),
            dbc.Col(
                dbc.RadioItems(
                    id='cargo-toggle',
                    options=[
                        {'label': 'Prefeito', 'value': 'Prefeito'},
                        {'label': 'Vereador', 'value': 'Vereador'}
                    ],
                    value='Prefeito',
                    inline=True,
                    className="btn-group btn-group-toggle",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary"
                ),
                width=6
            ),
        ], className="mb-4"),

        # Dropdown para selecionar múltiplos bairros
        dbc.Row([
            dbc.Col(html.Label('Selecione o(s) Bairro(s):', className="h5 font-weight-bold")),
            dbc.Col(
                dcc.Dropdown(
                    id='bairro-dropdown',
                    multi=True,
                    style={'width': '100%'}
                ),
                width=6
            )
        ], className="mb-4"),

        # Dropdown para selecionar múltiplos partidos
        dbc.Row([
            dbc.Col(html.Label('Selecione o(s) Partido(s):', className="h5 font-weight-bold")),
            dbc.Col(
                dcc.Dropdown(
                    id='partido-dropdown',
                    multi=True,
                    style={'width': '100%'}
                ),
                width=6
            )
        ], className="mb-4"),

        # Gráfico interativo
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='votos-graph', style={'height': '600px'})
            )
        ]),

        # Tabela de resultados
        html.H3("Resultados Detalhados", className="text-center my-4"),
        html.Div(id='tabela-resultados', style={'padding': '20px', 'maxHeight': '500px', 'overflowY': 'auto'})
    ], fluid=True)

    return layout
