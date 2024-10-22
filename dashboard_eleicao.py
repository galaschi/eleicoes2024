import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  # Importando Bootstrap

# Leitura dos dados
resultados_nh_vereador_agrupados = pd.read_csv("data/resultados_nh_vereador_agrupados.csv")
resultados_nh_prefeito_agrupados = pd.read_csv("data/resultados_nh_prefeito_agrupados.csv")
resultados_nh_vereador_bairro = pd.read_csv("data/total_votos_vereador_por_bairro.csv")
resultados_nh_prefeito_bairro = pd.read_csv("data/total_votos_prefeito_por_bairro.csv")

# Renomeando as colunas
resultados_nh_vereador_bairro.rename(columns={
    'NM_VOTAVEL': 'Nome Candidato',
    'SG_PARTIDO': 'Partido',
    'BAIRRO': 'Bairro',
    'QT_VOTOS': 'Total de Votos'
}, inplace=True)

resultados_nh_prefeito_bairro.rename(columns={
    'NM_VOTAVEL': 'Nome Candidato',
    'SG_PARTIDO': 'Partido',
    'BAIRRO': 'Bairro',
    'QT_VOTOS': 'Total de Votos'
}, inplace=True)

# Definindo df_prefeito e df_vereador
df_prefeito = resultados_nh_prefeito_bairro
df_vereador = resultados_nh_vereador_bairro

# Inicializar o aplicativo Dash com Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout do dashboard
app.layout = dbc.Container([
    html.H1("Resultados Eleições 2024 - Novo Hamburgo", className="text-center my-4", style={'color': '#4B0082'}),

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
                inline=True,  # Estilo inline como um toggle
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
            dcc.Graph(id='votos-graph', style={'height': '600px'})  # Aumentar a altura do gráfico
        )
    ]),

    # Tabela de resultados
    html.H3("Resultados Detalhados", className="text-center my-4"),
    html.Div(id='tabela-resultados', style={'padding': '20px', 'maxHeight': '500px', 'overflowY': 'auto'})
], fluid=True)


# Atualizar o dropdown de bairros de acordo com o cargo selecionado
@app.callback(
    [Output('bairro-dropdown', 'options'), Output('bairro-dropdown', 'value')],
    Input('cargo-toggle', 'value')
)
def atualizar_bairros(cargo):
    if cargo == 'Prefeito':
        bairros = df_prefeito['Bairro'].unique()
    else:
        bairros = df_vereador['Bairro'].unique()

    # Adicionar a opção "Todos" no início da lista de bairros
    options = [{'label': 'Todos', 'value': 'Todos'}] + [{'label': bairro, 'value': bairro} for bairro in bairros]
    return options, ['Todos']  # Definir "Todos" como valor padrão


# Atualizar o dropdown de partidos de acordo com o cargo selecionado
@app.callback(
    Output('partido-dropdown', 'options'),
    Input('cargo-toggle', 'value')
)
def atualizar_partidos(cargo):
    if cargo == 'Prefeito':
        partidos = df_prefeito['Partido'].unique()
    else:
        partidos = df_vereador['Partido'].unique()

    return [{'label': partido, 'value': partido} for partido in partidos]


# Atualizar o gráfico e a tabela com base na seleção de bairro, cargo e partido
@app.callback(
    [Output('votos-graph', 'figure'), Output('tabela-resultados', 'children')],
    [Input('cargo-toggle', 'value'), Input('bairro-dropdown', 'value'), Input('partido-dropdown', 'value')]
)
def atualizar_dashboard(cargo, bairros, partidos):
    if cargo == 'Prefeito':
        df = df_prefeito
    else:
        df = df_vereador

    # Filtrar os dados pelo(s) bairro(s) e partido(s) selecionado(s)
    if 'Todos' in bairros or not bairros:
        # Se "Todos" for selecionado ou nenhum bairro for selecionado, agrupar os dados por Partido e Nome Candidato, somando os votos
        df_filtrado = df.groupby(['Partido', 'Nome Candidato']).agg({'Total de Votos': 'sum'}).reset_index()
    else:
        df_filtrado = df[df['Bairro'].isin(bairros)]

    if partidos:
        df_filtrado = df_filtrado[df_filtrado['Partido'].isin(partidos)]

    # Ordenar os resultados por quantidade de votos em ordem decrescente
    df_filtrado = df_filtrado.sort_values(by='Total de Votos', ascending=False)

    # Gráfico: Votos por partido
    fig = px.bar(df_filtrado, x='Partido', y='Total de Votos', color='Nome Candidato',
                 title=f"Votos ({cargo})", height=600)

    # Tabela: Exibir resultados detalhados com estilo
    tabela_html = html.Table(
        # Cabeçalho da tabela
        [html.Thead(html.Tr([html.Th(col) for col in df_filtrado.columns]))] +
        # Corpo da tabela com alternância de cor nas linhas
        [html.Tbody([
            html.Tr([html.Td(df_filtrado.iloc[i][col]) for col in df_filtrado.columns],
                    style={'backgroundColor': '#f9f9f9' if i % 2 == 0 else '#e0e0e0'})
            for i in range(len(df_filtrado))
        ])],
        style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'border': '1px solid black',
            'textAlign': 'center',
            'fontSize': '16px'
        }
    )

    return fig, tabela_html


# Rodar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
