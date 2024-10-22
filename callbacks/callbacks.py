import plotly.express as px
from dash import html
from dash import Input, Output
import pandas as pd

# Leitura dos dados
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

def register_callbacks(app):
    @app.callback(
        [Output('bairro-dropdown', 'options'), Output('bairro-dropdown', 'value')],
        Input('cargo-toggle', 'value')
    )
    def atualizar_bairros(cargo):
        if cargo == 'Prefeito':
            bairros = df_prefeito['Bairro'].unique()
        else:
            bairros = df_vereador['Bairro'].unique()

        options = [{'label': 'Todos', 'value': 'Todos'}] + [{'label': bairro, 'value': bairro} for bairro in bairros]
        return options, ['Todos']  # Definir "Todos" como valor padrão

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

    @app.callback(
        [Output('votos-graph', 'figure'), Output('tabela-resultados', 'children')],
        [Input('cargo-toggle', 'value'), Input('bairro-dropdown', 'value'), Input('partido-dropdown', 'value')]
    )
    def atualizar_dashboard(cargo, bairros, partidos):
        if cargo == 'Prefeito':
            df = df_prefeito
        else:
            df = df_vereador

        if 'Todos' in bairros or not bairros:
            df_filtrado = df.groupby(['Partido', 'Nome Candidato']).agg({'Total de Votos': 'sum'}).reset_index()
        else:
            df_filtrado = df[df['Bairro'].isin(bairros)]

        if partidos:
            df_filtrado = df_filtrado[df_filtrado['Partido'].isin(partidos)]

        df_filtrado = df_filtrado.sort_values(by='Total de Votos', ascending=False)

        fig = px.bar(df_filtrado, x='Partido', y='Total de Votos', color='Nome Candidato',
                     title=f"Votos ({cargo})", height=600)

        tabela_html = html.Table(
            [html.Thead(html.Tr([html.Th(col) for col in df_filtrado.columns]))] +
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
