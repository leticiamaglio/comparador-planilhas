"""
chave.py

Funções relacionadas às colunas-chave da comparação.
"""

import pandas as pd
import streamlit as st
def escolher_chaves(df_a, df_b):

    st.subheader("🔑 Colunas-chave")

    col1, col2 = st.columns(2)

    with col1:

        chave_a = st.selectbox(
            "Planilha A",
            options=df_a.columns
        )

    with col2:

        chave_b = st.selectbox(
            "Planilha B",
            options=df_b.columns
        )

    return chave_a, chave_b

def validar_chaves(df, chaves):

    # Verifica se todas as colunas existem
    colunas_inexistentes = [
        coluna
        for coluna in chaves
        if coluna not in df.columns
    ]

    if colunas_inexistentes:

        raise ValueError(
            "As seguintes colunas-chave não foram encontradas na planilha: "
            + ", ".join(colunas_inexistentes)
        )

    duplicados = df[
        df.duplicated(
            subset=chaves,
            keep=False
        )
    ].copy()

    if duplicados.empty:

        return True, pd.DataFrame()

    return False, duplicados

def montar_mapeamento(
    df_a,
    df_b,
    chaves
):

    st.subheader("🧩 Mapeamento das Colunas")

    colunas_a = [
        c
        for c in df_a.columns
        if c not in chaves
    ]

    colunas_b = [
        c
        for c in df_b.columns
        if c not in chaves
    ]

    mapeamento = {}

    for coluna in colunas_a:

        indice = (
            colunas_b.index(coluna) + 1
            if coluna in colunas_b
            else 0
        )

        escolha = st.selectbox(
            f"{coluna} →",
            options=["Não comparar"] + colunas_b,
            index=indice,
            key=f"map_{coluna}"
        )

        mapeamento[coluna] = escolha

    return mapeamento