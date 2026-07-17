"""
Modelos de dados da aplicação.
"""

from dataclasses import dataclass

import pandas as pd


@dataclass
class ResumoComparacao:

    nome_planilha_a: str
    nome_planilha_b: str

    total_planilha_a: int
    total_planilha_b: int

    consistentes: int
    exclusivos_a: int
    exclusivos_b: int
    inconsistentes: int
    consolidado: int


@dataclass
class ResultadoComparacao:

    resumo: ResumoComparacao

    consistentes: pd.DataFrame

    exclusivos_a: pd.DataFrame

    exclusivos_b: pd.DataFrame

    inconsistentes: pd.DataFrame

    consolidado: pd.DataFrame