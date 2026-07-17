"""Extratores determinísticos e registráveis, independentes da interface."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class ResultadoExtracao:
    valor: Any | None
    status: str
    mensagem: str | None = None


Extrator = Callable[[Any], ResultadoExtracao]


class RegistroExtratores:
    def __init__(self) -> None:
        self._extratores: dict[str, Extrator] = {}

    def registrar(self, identificador: str, extrator: Extrator) -> None:
        if identificador in self._extratores:
            raise ValueError(f"Extrator já registrado: {identificador!r}.")
        self._extratores[identificador] = extrator

    def extrair(self, identificador: str, valor: Any) -> ResultadoExtracao:
        return self.obter(identificador)(valor)

    def obter(self, identificador: str) -> Extrator:
        try:
            return self._extratores[identificador]
        except KeyError as erro:
            raise ValueError(f"Extrator desconhecido: {identificador!r}.") from erro

    def listar_ids(self) -> tuple[str, ...]:
        return tuple(self._extratores)


def _texto(valor: Any) -> str:
    return "" if valor is None or pd.isna(valor) else str(valor)


def extrair_numero_nf(valor: Any) -> ResultadoExtracao:
    texto = _texto(valor)

    padroes = [

        # NF 12345
        r"\bnf\s*([a-z0-9]+)\b",

        # Nota Fiscal 12345
        r"\bnota\s+fiscal\s*(?:n[ºo.]?\s*)?([a-z0-9]+)\b",

        # FAT 617086
        r"\bfat\s*([a-z0-9]+)\b",

        # ND 12481487
        r"\bnd\s*([a-z0-9]+)\b",

    ]

    encontrados = []

    for padrao in padroes:
        encontrados.extend(
            re.findall(
                padrao,
                texto,
                flags=re.IGNORECASE
            )
        )

    encontrados = list(dict.fromkeys(encontrados))

    if len(encontrados) == 1:
        return ResultadoExtracao(
            encontrados[0],
            "extraido"
        )

    if len(encontrados) > 1:
        return ResultadoExtracao(
            None,
            "ambigua_extracao",
            f"Foram encontrados {len(encontrados)} possíveis números."
        )

    return ResultadoExtracao(
        None,
        "falha_extracao",
        "Número da nota não encontrado."
    )


def extrair_valor_monetario(valor: Any) -> ResultadoExtracao:
    texto = _texto(valor)
    encontrados = re.findall(r"R\$\s*([\d.]+(?:,[0-9]{1,2})?|\d+(?:\.\d{1,2})?)", texto, re.IGNORECASE)
    if len(encontrados) == 1:
        return ResultadoExtracao(encontrados[0], "extraido")
    if len(encontrados) > 1:
        return ResultadoExtracao(None, "ambigua_extracao", "Mais de um valor encontrado.")
    return ResultadoExtracao(None, "falha_extracao", "Valor monetário não encontrado.")


def extrair_fornecedor_arquivo_nf(valor: Any) -> ResultadoExtracao:
    texto = _texto(valor)
    if not texto:
        return ResultadoExtracao(None, "falha_extracao", "Texto vazio.")
    fornecedor = re.sub(r"\b(?:n\.?\s*f\.?|nota\s+fiscal)\s*(?:n[ºo.]?\s*)?\d+\b", "", texto, flags=re.IGNORECASE)
    fornecedor = re.sub(r"R\$\s*[\d.]+(?:,[0-9]{1,2})?", "", fornecedor, flags=re.IGNORECASE)
    fornecedor = re.sub(r"\.(pdf|xlsx?|csv)$", "", fornecedor, flags=re.IGNORECASE).strip(" -_ ")
    if fornecedor:
        return ResultadoExtracao(fornecedor, "extraido")
    return ResultadoExtracao(None, "falha_extracao", "Fornecedor não encontrado.")


EXTRATORES_PADRAO = RegistroExtratores()
EXTRATORES_PADRAO.registrar("numero_nf", extrair_numero_nf)
EXTRATORES_PADRAO.registrar("valor_monetario", extrair_valor_monetario)
EXTRATORES_PADRAO.registrar("fornecedor_arquivo_nf", extrair_fornecedor_arquivo_nf)
