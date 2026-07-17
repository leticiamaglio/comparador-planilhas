import streamlit as st
from reconciliador.exportador import gerar_excel
from reconciliador.interface import (
    aplicar_estilo,
    botao_comparar,
    botao_download,
    configurar_pagina,
    mostrar_dashboard_v2,
    mostrar_preview,
    mostrar_resultados_v2,
    mostrar_sidebar_v2,
    mostrar_titulo,
    upload_planilhas,
)
from reconciliador.leitor import ler_planilha
from reconciliador.v2 import CATALOGO_PADRAO, Padronizador
from reconciliador.v2.extratores import EXTRATORES_PADRAO
from reconciliador.v2.interface import mostrar_mapeamento_conceitos
from reconciliador.v2.reconciliador import Reconciliador


configurar_pagina()
aplicar_estilo()
mostrar_titulo()
mostrar_sidebar_v2()

arquivo_a, arquivo_b = upload_planilhas()
if arquivo_a is None or arquivo_b is None:
    st.stop()

st.subheader("Configuração da leitura")
coluna_a, coluna_b = st.columns(2)
with coluna_a:
    cabecalho_a = st.number_input("Cabeçalho da Planilha A começa na linha", min_value=1, value=1, step=1)
with coluna_b:
    cabecalho_b = st.number_input("Cabeçalho da Planilha B começa na linha", min_value=1, value=1, step=1)

try:
    dados_a = ler_planilha(arquivo_a, cabecalho=cabecalho_a - 1)
    dados_b = ler_planilha(arquivo_b, cabecalho=cabecalho_b - 1)
except Exception as erro:
    st.error("Não foi possível abrir uma das planilhas.")
    st.exception(erro)
    st.stop()

mostrar_preview(dados_a, dados_b)
st.divider()
config_a, config_b, especificacao = mostrar_mapeamento_conceitos(dados_a, dados_b, CATALOGO_PADRAO)
st.divider()

if botao_comparar():
    try:
        padronizador = Padronizador(CATALOGO_PADRAO, EXTRATORES_PADRAO)

        resultado_a = padronizador.executar(dados_a, config_a)
        resultado_b = padronizador.executar(dados_b, config_b)

        for aviso in resultado_a.avisos + resultado_b.avisos:
            st.warning(aviso)

        resultado = Reconciliador().executar(
            resultado_a.dados,
            resultado_b.dados,
            especificacao
        )

    except ValueError as erro:
        st.error(str(erro))
        st.stop()

    st.divider()

mostrar_dashboard_v2(resultado, list(especificacao.chaves))
mostrar_resultados_v2(resultado)

botao_download(gerar_excel(resultado))