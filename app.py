import os
import subprocess
from dash import Dash
import dash_bootstrap_components as dbc
from layouts.layout import create_layout

# Caminho do script data.py
data_script_path = os.path.join(os.getcwd(), 'data', 'data.py')

# Verifica se os arquivos CSV existem
csv_files = [
    'data/resultados_nh_vereador_agrupados.csv',
    'data/resultados_nh_prefeito_agrupados.csv',
    'data/total_votos_vereador_por_bairro.csv',
    'data/total_votos_prefeito_por_bairro.csv'
]

# Função para verificar se todos os arquivos existem
def check_csv_files(files):
    return all([os.path.exists(f) for f in files])

# Se os arquivos não existirem, executa o script data.py
if not check_csv_files(csv_files):
    print("Arquivos CSV não encontrados, gerando arquivos...")
    subprocess.run(['python', data_script_path], check=True)
else:
    print("Todos os arquivos CSV já estão presentes.")

# Inicializar o aplicativo Dash com Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configurar o layout
app.layout = create_layout()

# Importar callbacks
from callbacks.callbacks import register_callbacks
register_callbacks(app)  # Chame a função que registra os callbacks

# Rodar o aplicativo
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)
