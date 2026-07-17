"""
normalizacao.py

Normalização inteligente de valores antes da comparação.

Autor: Letícia Maglio
"""

from __future__ import annotations

import re
import unicodedata

from datetime import datetime
from typing import Any

import pandas as pd


# ==========================================================
# REGEX
# ==========================================================

RE_DIGITOS = re.compile(r"\D")

RE_ESPACOS = re.compile(r"\s+")

RE_NUMERO = re.compile(
    r"^[+-]?\d[\d., ]*$"
)

RE_TELEFONE = re.compile(
    r"^[\d()\-\+\s]+$"
)

RE_DOCUMENTO = re.compile(
    r"^[\d./\-]+$"
)


# ==========================================================
# UTILIDADES
# ==========================================================

def _somente_digitos(texto: str) -> str:

    return RE_DIGITOS.sub("", texto)


def _texto(valor: Any) -> str:

    if valor is None:
        return ""

    return str(valor)


def _eh_vazio(valor: Any) -> bool:

    try:
        return pd.isna(valor)
    except Exception:
        return False


# ==========================================================
# TEXTO
# ==========================================================

def _remover_acentos(texto: str) -> str:

    return "".join(

        caractere

        for caractere in unicodedata.normalize(
            "NFKD",
            texto
        )

        if not unicodedata.combining(caractere)

    )


def _remover_caracteres_invisiveis(
    texto: str
) -> str:

    caracteres = (

        "\u00A0",
        "\u200B",
        "\u200C",
        "\u200D",
        "\ufeff"

    )

    for caractere in caracteres:

        texto = texto.replace(
            caractere,
            " "
        )

    return texto


def _normalizar_espacos(
    texto: str
) -> str:

    return RE_ESPACOS.sub(
        " ",
        texto
    ).strip()
# ==========================================================
# DETECTORES
# ==========================================================

def _parece_documento(texto: str) -> bool:
    """
    Verifica se o valor parece ser um CPF ou CNPJ.
    """

    if not RE_DOCUMENTO.fullmatch(texto.strip()):
        return False

    numeros = _somente_digitos(texto)

    if len(numeros) not in (11, 14):
        return False

    # evita 00000000000 / 11111111111 etc.
    if len(set(numeros)) == 1:
        return False

    return True


def _parece_telefone(texto: str) -> bool:
    """
    Verifica se o valor parece um telefone brasileiro.
    """

    if not RE_TELEFONE.fullmatch(texto.strip()):
        return False

    numeros = _somente_digitos(texto)

    if numeros.startswith("55") and len(numeros) > 11:
        numeros = numeros[2:]

    return len(numeros) in (10, 11)


def _parece_numero(texto: str) -> bool:
    """
    Verifica se o valor parece um número.
    """

    texto = texto.strip()

    if texto == "":
        return False

    return bool(RE_NUMERO.fullmatch(texto))


def _parece_data(texto: str) -> bool:
    """
    Verifica se o valor pode ser interpretado como data.
    """

    texto = texto.strip()

    if texto == "":
        return False

    formatos = (

        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y%m%d"

    )

    for formato in formatos:

        try:

            datetime.strptime(
                texto,
                formato
            )

            return True

        except Exception:

            pass

    try:

        pd.to_datetime(
            texto,
            dayfirst=True,
            errors="raise"
        )

        return True

    except Exception:

        return False
    
# ==========================================================
# DOCUMENTOS
# ==========================================================

def _normalizar_documento(texto: str) -> str:
    """
    Remove qualquer pontuação de CPF/CNPJ.
    """

    return _somente_digitos(texto)


# ==========================================================
# TELEFONES
# ==========================================================

def _normalizar_telefone(texto: str) -> str:
    """
    Padroniza telefones brasileiros.

    Exemplos:

    +55 (11) 99999-9999
    (11)99999-9999
    11 99999 9999

    →

    11999999999
    """

    numeros = _somente_digitos(texto)

    # remove DDI
    if numeros.startswith("55") and len(numeros) > 11:
        numeros = numeros[2:]

    # remove zero de longa distância
    if numeros.startswith("0") and len(numeros) > 10:
        numeros = numeros[1:]

    return numeros


# ==========================================================
# TEXTO
# ==========================================================

def _normalizar_texto(
    texto: str,
    opcoes: dict
):

    texto = _remover_caracteres_invisiveis(texto)

    if opcoes.get(
        "ignorar_espacos",
        True
    ):

        texto = _normalizar_espacos(texto)

    if opcoes.get(
        "ignorar_maiusculas",
        True
    ):

        texto = texto.casefold()

    if opcoes.get(
        "ignorar_acentos",
        True
    ):

        texto = _remover_acentos(texto)

    return texto
# ==========================================================
# NÚMEROS
# ==========================================================

def _normalizar_numero(texto: str):
    """
    Converte números em um formato único.

    Exemplos:

    10 -> 10.0
    10,00 -> 10.0
    10.00 -> 10.0

    1.234,56 -> 1234.56
    1,234.56 -> 1234.56

    1.000 -> 1000
    1,000 -> 1000

    1.5 -> 1.5
    1,5 -> 1.5
    """

    texto = texto.strip()

    if texto == "":
        return texto

    texto = texto.replace(" ", "")

    try:

        # ------------------------------------------
        # Tem ponto E vírgula
        # ------------------------------------------

        if "." in texto and "," in texto:

            if texto.rfind(",") > texto.rfind("."):

                # Brasileiro
                # 1.234,56

                texto = texto.replace(".", "")
                texto = texto.replace(",", ".")

            else:

                # Americano
                # 1,234.56

                texto = texto.replace(",", "")

        # ------------------------------------------
        # Apenas vírgula
        # ------------------------------------------

        elif "," in texto:

            partes = texto.split(",")

            if len(partes[-1]) == 3:

                # 1,000

                texto = "".join(partes)

            else:

                # 1,5

                texto = texto.replace(",", ".")

        # ------------------------------------------
        # Apenas ponto
        # ------------------------------------------

        elif "." in texto:

            partes = texto.split(".")

            if len(partes[-1]) == 3:

                # 1.000

                texto = "".join(partes)

        return float(texto)

    except Exception:

        return texto
# ==========================================================
# DATAS
# ==========================================================

_FORMATOS_DATA = (

    "%d/%m/%Y",
    "%d-%m-%Y",

    "%Y-%m-%d",
    "%Y/%m/%d",

    "%d/%m/%y",
    "%d-%m-%y",

    "%Y%m%d"

)


def _normalizar_data(valor):
    """
    Converte diferentes formatos de data
    para YYYY-MM-DD.
    """

    if isinstance(valor, pd.Timestamp):

        return valor.strftime("%Y-%m-%d")

    if isinstance(valor, datetime):

        return valor.strftime("%Y-%m-%d")

    texto = str(valor).strip()

    if texto == "":

        return texto

    # tenta formatos conhecidos

    for formato in _FORMATOS_DATA:

        try:

            data = datetime.strptime(
                texto,
                formato
            )

            return data.strftime(
                "%Y-%m-%d"
            )

        except Exception:

            pass

    # tenta parser do pandas

    try:

        data = pd.to_datetime(

            texto,

            dayfirst=True,

            errors="raise"

        )

        return data.strftime(
            "%Y-%m-%d"
        )

    except Exception:

        return valor
# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def preparar_valor(
    valor,
    opcoes
):
    """
    Prepara um valor para comparação.

    A ordem das normalizações é importante.

    Documento
        ↓
    Telefone
        ↓
    Número
        ↓
    Data
        ↓
    Texto
    """

    # ------------------------------------------------------
    # Valor vazio
    # ------------------------------------------------------

    if _eh_vazio(valor):

        if opcoes.get(
            "vazios_iguais",
            True
        ):
            return ""

        return valor

    texto = _texto(valor)

    # ------------------------------------------------------
    # Documento
    # ------------------------------------------------------

    if (

        opcoes.get(
            "normalizar_documentos",
            True
        )

        and

        _parece_documento(texto)

    ):

        return _normalizar_documento(texto)

    # ------------------------------------------------------
    # Telefone
    # ------------------------------------------------------

    if (

        opcoes.get(
            "normalizar_telefones",
            True
        )

        and

        _parece_telefone(texto)

    ):

        return _normalizar_telefone(texto)

    # ------------------------------------------------------
    # Número
    # ------------------------------------------------------

    if (

        opcoes.get(
            "normalizar_numeros",
            False
        )

        and

        _parece_numero(texto)

    ):

        return _normalizar_numero(texto)

    # ------------------------------------------------------
    # Data
    # ------------------------------------------------------

    if (

        opcoes.get(
            "normalizar_datas",
            False
        )

        and

        _parece_data(texto)

    ):

        return _normalizar_data(texto)

    # ------------------------------------------------------
    # Texto
    # ------------------------------------------------------

    return _normalizar_texto(
        texto,
        opcoes
    )