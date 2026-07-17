"""
configuracoes.py

Responsável pelas opções avançadas da comparação.
"""

import streamlit as st


def mostrar_opcoes():

    with st.expander("⚙️ Opções Avançadas"):

        st.caption(
            "Personalize como os valores serão comparados entre as planilhas."
        )

        ignorar_maiusculas = st.checkbox(
            "Ignorar diferenças entre maiúsculas e minúsculas",
            value=True
        )

        ignorar_espacos = st.checkbox(
            "Ignorar espaços no início e fim do texto",
            value=True
        )

        vazios_iguais = st.checkbox(
            "Considerar células vazias como iguais",
            value=True
        )

        ignorar_acentos = st.checkbox(
            "Ignorar acentos (José = Jose)",
            value=True
        )

        normalizar_documentos = st.checkbox(
            "Padronizar CPF/CNPJ",
            value=True
        )

        normalizar_telefones = st.checkbox(
            "Padronizar telefones",
            value=True
        )

        normalizar_numeros = st.checkbox(
            "Normalizar números automaticamente (10 = 10,00)",
            value=False
        )

        normalizar_datas = st.checkbox(
            "Normalizar datas automaticamente",
            value=False
        )

    return {

    "ignorar_maiusculas": ignorar_maiusculas,

    "ignorar_espacos": ignorar_espacos,

    "ignorar_acentos": ignorar_acentos,

    "vazios_iguais": vazios_iguais,

    "normalizar_documentos": normalizar_documentos,

    "normalizar_telefones": normalizar_telefones,

    "normalizar_numeros": normalizar_numeros,

    "normalizar_datas": normalizar_datas

}