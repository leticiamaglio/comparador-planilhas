"""
Leitura e preparação das planilhas.
"""

import pandas as pd


FORMATOS_SUPORTADOS = (
    ".xlsx",
    ".xls",
    ".csv"
)


def ler_planilha(arquivo):

    nome = arquivo.name.lower()

    if nome.endswith(".csv"):

        df = pd.read_csv(arquivo)

    elif nome.endswith((".xlsx", ".xls")):

        df = pd.read_excel(arquivo)

    else:

        raise ValueError(
            "Formato de arquivo não suportado."
        )

    df = limpar_dataframe(df)

    return df


def limpar_dataframe(df):

    df = df.copy()

    df.dropna(
        how="all",
        inplace=True
    )

    df.dropna(
        axis=1,
        how="all",
        inplace=True
    )

    df.columns = [
        str(coluna).strip()
        for coluna in df.columns
    ]

    for coluna in df.columns:

        if df[coluna].dtype == object:

            df[coluna] = (
                df[coluna]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df