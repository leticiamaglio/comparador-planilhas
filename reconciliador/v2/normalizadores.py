"""Normalização orientada pelo tipo semântico do conceito."""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal, InvalidOperation
from typing import Any

import pandas as pd

from reconciliador.v2.modelos import TipoDado


def _vazio(valor: Any) -> bool:
    return valor is None or (not isinstance(valor, str) and pd.isna(valor))


def _texto(valor: Any) -> str:
    texto = str(valor).replace("\u00a0", " ").strip()
    texto = " ".join(texto.split()).casefold()
    return "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))


def _decimal(valor: Any) -> Decimal:
    texto = str(valor).strip().replace("R$", "").replace(" ", "")
    if "." in texto and "," in texto:
        texto = texto.replace(".", "").replace(",", ".") if texto.rfind(",") > texto.rfind(".") else texto.replace(",", "")
    elif "," in texto:
        partes = texto.split(",")
        texto = "".join(partes) if len(partes[-1]) == 3 else texto.replace(",", ".")
    elif "." in texto:
        partes = texto.split(".")
        if len(partes[-1]) == 3:
            texto = "".join(partes)
    return Decimal(texto).quantize(Decimal("0.01"))


def normalizar(valor: Any, tipo: TipoDado) -> Any | None:
    if _vazio(valor) or str(valor).strip() == "":
        return None
    if tipo is TipoDado.DOCUMENTO:
        return re.sub(r"\D", "", str(valor))
    if tipo is TipoDado.DECIMAL:
        try:
            return _decimal(valor)
        except (InvalidOperation, ValueError):
            return _texto(valor)
    if tipo is TipoDado.DATA:
        data = pd.to_datetime(valor, dayfirst=True, errors="coerce")
        return data.strftime("%Y-%m-%d") if not pd.isna(data) else _texto(valor)
    if tipo is TipoDado.IDENTIFICADOR:
        return re.sub(r"\s+", "", str(valor)).casefold()
    return _texto(valor)
