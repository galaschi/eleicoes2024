import pandas as pd

# Consolidado de resultados de Novo Hamburgo
codigo_novo_hamburgo = 87718
resultados_rs_2024 = pd.read_csv("resultados_rs_2024.csv", sep=';', encoding='ISO-8859-1')
secoes_nh = pd.read_csv("secoes_nh.csv", sep=';')
resultados_nh = resultados_rs_2024[resultados_rs_2024['CD_MUNICIPIO'] == codigo_novo_hamburgo]
merged_resultados_nh = pd.merge(
    resultados_nh,
    secoes_nh[['NR_ZONA', 'NR_SECAO', 'NM_SECAO', 'ENDERECO', 'BAIRRO']],
    on=['NR_SECAO', 'NR_ZONA'],
    how='inner'
)

# Resultados a Prefeito
resultados_nh_prefeito = merged_resultados_nh[merged_resultados_nh['DS_CARGO_PERGUNTA'] == 'Prefeito']
resultados_nh_prefeito_agrupados = resultados_nh_prefeito.groupby(['NM_VOTAVEL', 'SG_PARTIDO', 'NR_SECAO', 'NM_SECAO', 'ENDERECO', 'BAIRRO'])['QT_VOTOS'].sum().reset_index()
total_votos_prefeito_por_candidato = resultados_nh_prefeito_agrupados.groupby('NM_VOTAVEL')['QT_VOTOS'].sum().reset_index()
total_votos_prefeito_por_partido = resultados_nh_prefeito_agrupados.groupby('SG_PARTIDO')['QT_VOTOS'].sum().reset_index()
total_votos_prefeito_por_bairro = resultados_nh_prefeito_agrupados.groupby(['NM_VOTAVEL', 'SG_PARTIDO', 'BAIRRO'])['QT_VOTOS'].sum().reset_index()

# Resultados a Vereador
resultados_nh_vereador = merged_resultados_nh[merged_resultados_nh['DS_CARGO_PERGUNTA'] == 'Vereador']
resultados_nh_vereador_agrupados = resultados_nh_vereador.groupby(['NM_VOTAVEL', 'SG_PARTIDO', 'NR_SECAO', 'NM_SECAO', 'ENDERECO', 'BAIRRO'])['QT_VOTOS'].sum().reset_index()
total_votos_vereador_por_candidato = resultados_nh_vereador_agrupados.groupby('NM_VOTAVEL')['QT_VOTOS'].sum().reset_index()
total_votos_vereador_por_partido = resultados_nh_vereador_agrupados.groupby('SG_PARTIDO')['QT_VOTOS'].sum().reset_index()
total_votos_vereador_por_partido_bairro = resultados_nh_vereador_agrupados.groupby(['SG_PARTIDO', 'BAIRRO'])['QT_VOTOS'].sum().reset_index().sort_values(['BAIRRO', 'QT_VOTOS'], ascending=[True, False])
total_votos_vereador_por_bairro_ordenado = resultados_nh_vereador_agrupados.groupby(['NM_VOTAVEL', 'BAIRRO'])['QT_VOTOS'].sum().reset_index().sort_values(['BAIRRO', 'QT_VOTOS'], ascending=[True, False])
total_votos_vereador_por_bairro = resultados_nh_vereador_agrupados.groupby(['NM_VOTAVEL', 'SG_PARTIDO', 'BAIRRO'])['QT_VOTOS'].sum().reset_index()

# CSVs
resultados_nh_prefeito_agrupados.to_csv("resultados_nh_prefeito_agrupados.csv", index=False)
resultados_nh_vereador_agrupados.to_csv("resultados_nh_vereador_agrupados.csv", index=False)
total_votos_vereador_por_bairro.to_csv("total_votos_vereador_por_bairro.csv", index=False)
total_votos_prefeito_por_bairro.to_csv("total_votos_prefeito_por_bairro.csv", index=False)
