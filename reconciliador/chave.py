"""
chave.py

Funções relacionadas às colunas-chave da comparação.
"""

import pandas as pd
import streamlit as st


def escolher_chaves(df):

    return st.multiselect(
        "🔑 Selecione a(s) coluna(s)-chave",
        options=list(df.columns),
        default=[df.columns[0]]
    )


def validar_chaves(df, chaves):

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