"""Reconciliação de datasets canônicos, sem conhecimento do layout de origem."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from reconciliador.v2.modelos import EspecificacaoReconciliacao


@dataclass
class ResumoReconciliacao:
    nome_planilha_a: str
    nome_planilha_b: str
    total_planilha_a: int
    total_planilha_b: int
    consistentes: int
    inconsistentes: int
    exclusivos_a: int
    exclusivos_b: int
    duplicados_a: int
    duplicados_b: int
    sem_chave_a: int
    sem_chave_b: int
    consolidado: int


@dataclass
class ResultadoReconciliacao:
    resumo: ResumoReconciliacao
    consistentes: pd.DataFrame
    inconsistentes: pd.DataFrame
    exclusivos_a: pd.DataFrame
    exclusivos_b: pd.DataFrame
    duplicados_a: pd.DataFrame
    duplicados_b: pd.DataFrame
    sem_chave_a: pd.DataFrame
    sem_chave_b: pd.DataFrame
    consolidado: pd.DataFrame


class Reconciliador:
    def executar(
        self,
        dados_a: pd.DataFrame,
        dados_b: pd.DataFrame,
        especificacao: EspecificacaoReconciliacao,
    ) -> ResultadoReconciliacao:
        self._validar(dados_a, dados_b, especificacao)
        trabalho_a = dados_a.copy()
        trabalho_b = dados_b.copy()
        chave_a = self._chaves(trabalho_a, especificacao.chaves)
        chave_b = self._chaves(trabalho_b, especificacao.chaves)
        trabalho_a["_chave_reconciliacao"] = chave_a
        trabalho_b["_chave_reconciliacao"] = chave_b

        sem_chave_a = trabalho_a[trabalho_a["_chave_reconciliacao"].isna()].copy()
        sem_chave_b = trabalho_b[trabalho_b["_chave_reconciliacao"].isna()].copy()
        validos_a = trabalho_a[trabalho_a["_chave_reconciliacao"].notna()].copy()
        validos_b = trabalho_b[trabalho_b["_chave_reconciliacao"].notna()].copy()

        duplicados_a = self._duplicados(validos_a)
        duplicados_b = self._duplicados(validos_b)
        unicos_a = validos_a[~validos_a["_chave_reconciliacao"].duplicated(keep=False)].copy()
        unicos_b = validos_b[~validos_b["_chave_reconciliacao"].duplicated(keep=False)].copy()
        por_chave_a = {linha["_chave_reconciliacao"]: linha for _, linha in unicos_a.iterrows()}
        por_chave_b = {linha["_chave_reconciliacao"]: linha for _, linha in unicos_b.iterrows()}

        chaves_a, chaves_b = set(por_chave_a), set(por_chave_b)
        exclusivos_a = self._selecionar(por_chave_a, chaves_a - chaves_b, unicos_a.columns)
        exclusivos_b = self._selecionar(por_chave_b, chaves_b - chaves_a, unicos_b.columns)
        consistentes, inconsistentes = self._comparar_comuns(
            por_chave_a, por_chave_b, chaves_a & chaves_b, especificacao.campos_comparados
        )
        consolidado = pd.concat(
            [consistentes, exclusivos_a, exclusivos_b], ignore_index=True
        ).drop(columns=["_chave_reconciliacao"], errors="ignore").drop_duplicates().reset_index(drop=True)
        resumo = ResumoReconciliacao(
            nome_planilha_a=str(dados_a["_origem"].iloc[0]) if not dados_a.empty else "Planilha A",
            nome_planilha_b=str(dados_b["_origem"].iloc[0]) if not dados_b.empty else "Planilha B",
            total_planilha_a=len(dados_a), total_planilha_b=len(dados_b),
            consistentes=len(consistentes), inconsistentes=len(inconsistentes) // 2,
            exclusivos_a=len(exclusivos_a), exclusivos_b=len(exclusivos_b),
            duplicados_a=len(duplicados_a), duplicados_b=len(duplicados_b),
            sem_chave_a=len(sem_chave_a), sem_chave_b=len(sem_chave_b), consolidado=len(consolidado),
        )
        return ResultadoReconciliacao(resumo, consistentes, inconsistentes, exclusivos_a, exclusivos_b,
                                      duplicados_a, duplicados_b, sem_chave_a, sem_chave_b, consolidado)

    @staticmethod
    def _validar(a: pd.DataFrame, b: pd.DataFrame, e: EspecificacaoReconciliacao) -> None:
        if not e.chaves:
            raise ValueError("Selecione ao menos um conceito como chave de reconciliação.")
        for conceito in set(e.chaves + e.campos_comparados):
            if conceito not in a.columns or conceito not in b.columns:
                raise ValueError(f"O conceito {conceito!r} deve estar mapeado nas duas planilhas.")

    @staticmethod
    def _chaves(dados: pd.DataFrame, chaves: tuple[str, ...]) -> pd.Series:
        def montar(linha: pd.Series):
            valores = tuple(linha[coluna] for coluna in chaves)
            return None if any(pd.isna(valor) or valor == "" for valor in valores) else valores
        return dados.loc[:, list(chaves)].apply(montar, axis=1)

    @staticmethod
    def _duplicados(dados: pd.DataFrame) -> pd.DataFrame:
        resultado = dados[dados["_chave_reconciliacao"].duplicated(keep=False)].copy()
        if not resultado.empty:
            resultado["Motivo"] = "Chave de reconciliação duplicada"
        return resultado

    @staticmethod
    def _selecionar(indice: dict, chaves: set[tuple], colunas) -> pd.DataFrame:
        if not chaves:
            return pd.DataFrame(columns=colunas)
        return pd.DataFrame([indice[chave].to_dict() for chave in chaves]).reset_index(drop=True)

    @staticmethod
    def _comparar_comuns(a: dict, b: dict, chaves: set[tuple], campos: tuple[str, ...]):
        consistentes, inconsistentes = [], []
        for chave in sorted(chaves, key=str):
            linha_a, linha_b = a[chave], b[chave]
            divergentes = [campo for campo in campos if linha_a[campo] != linha_b[campo]]
            if not divergentes:
                consistentes.append(linha_a.to_dict())
                continue
            motivo = "; ".join(divergentes)
            registro_a, registro_b = linha_a.to_dict(), linha_b.to_dict()
            registro_a.update({"Origem": "Planilha A", "Motivo da Inconsistência": motivo})
            registro_b.update({"Origem": "Planilha B", "Motivo da Inconsistência": motivo})
            inconsistentes.extend((registro_a, registro_b))
        return pd.DataFrame(consistentes), pd.DataFrame(inconsistentes)
