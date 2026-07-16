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

    try:

        if nome.endswith(".csv"):

            # tenta UTF-8 e, se falhar, Latin-1

            try:
                df = pd.read_csv(arquivo, encoding="utf-8")

            except UnicodeDecodeError:

                arquivo.seek(0)

                df = pd.read_csv(
                    arquivo,
                    encoding="latin1"
                )

        elif nome.endswith(".xlsx"):

            df = pd.read_excel(
                arquivo,
                engine="openpyxl"
            )

        elif nome.endswith(".xls"):

            df = pd.read_excel(
                arquivo,
                engine="xlrd"
            )

        else:

            raise ValueError(
                "Formato de arquivo não suportado."
            )

    except Exception as erro:

        raise ValueError(

            "Não foi possível abrir a planilha.\n\n"
            "Verifique se o arquivo não está corrompido "
            "e se possui uma extensão válida (.xlsx, .xls ou .csv).\n\n"
            f"Detalhes: {erro}"

        )

    return limpar_dataframe(df)

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