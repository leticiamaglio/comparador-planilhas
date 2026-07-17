"""
Perfil de Reconciliação de Notas Fiscais.

Transforma diferentes planilhas para
um modelo padrão.
"""

import re
import pandas as pd


# ==========================================================
# EXTRAÇÃO
# ==========================================================

def extrair_nf(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto)

    match = re.search(
        r"NF\s*(\d+)",
        texto,
        flags=re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


def extrair_valor(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto)

    match = re.search(
        r"R\$ ?([\d.,]+)",
        texto,
        flags=re.IGNORECASE
    )

    if not match:
        return ""

    valor = (
        match.group(1)
        .replace(".", "")
        .replace(",", ".")
    )

    try:
        return float(valor)

    except ValueError:
        return ""


def extrair_fornecedor(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto)

    texto = re.sub(
        r"NF\s*\d+",
        "",
        texto,
        flags=re.IGNORECASE
    )

    texto = re.sub(
        r"R\$ ?[\d.,]+",
        "",
        texto
    )

    texto = texto.replace(".pdf", "")

    return texto.strip()


# ==========================================================
# TRANSFORMAÇÃO
# ==========================================================

def transformar(df_a, df_b):

    """
    Ainda será implementado.
    Por enquanto apenas devolve
    as planilhas sem alteração.
    """

    return df_a.copy(), df_b.copy()