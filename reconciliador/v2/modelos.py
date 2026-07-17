"""Contratos de dados da etapa de padronização."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import pandas as pd


class TipoDado(str, Enum):
    TEXTO = "texto"
    IDENTIFICADOR = "identificador"
    DECIMAL = "decimal"
    DATA = "data"
    DOCUMENTO = "documento"


@dataclass(frozen=True)
class Conceito:
    """Definição estável de uma informação de negócio."""

    id: str
    nome: str
    tipo: TipoDado
    descricao: str = ""
    extratores_compativeis: tuple[str, ...] = ()


@dataclass(frozen=True)
class RegraCampo:
    """Como obter um conceito a partir de uma coluna de uma origem."""

    conceito_id: str
    coluna_origem: str
    extrator_id: str | None = None
    obrigatorio: bool = False


@dataclass(frozen=True)
class ConfiguracaoPadronizacao:
    """Configuração salva para uma planilha, sem dependência de Streamlit."""

    nome_origem: str
    campos: tuple[RegraCampo, ...]


@dataclass(frozen=True)
class EspecificacaoReconciliacao:
    """Define os conceitos usados para localizar e comparar registros."""

    chaves: tuple[str, ...]
    campos_comparados: tuple[str, ...]


@dataclass
class ResultadoPadronizacao:
    """
    Resultado produzido pelo Padronizador.

    dados:
        Dataset canônico utilizado pelo reconciliador.

    avisos:
        Resumo textual das ocorrências encontradas durante a padronização.

    pendencias_extracao:
        Registros em que algum conceito não pôde ser extraído
        automaticamente ou foi considerado ambíguo.
    """

    dados: pd.DataFrame

    avisos: list[str] = field(default_factory=list)

    pendencias_extracao: pd.DataFrame = field(
        default_factory=pd.DataFrame
    )
