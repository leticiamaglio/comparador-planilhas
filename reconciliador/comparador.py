"""
comparador.py

Responsável pela reconciliação entre duas planilhas.
"""

import pandas as pd

from reconciliador.modelos import (
    ResultadoComparacao,
    ResumoComparacao
)


class Comparador:

    def __init__(
        self,
        df_a,
        df_b,
        chaves,
        mapeamento,
        nome_planilha_a,
        nome_planilha_b
    ):

        self.df_a = df_a.copy()
        self.df_b = df_b.copy()

        self.chaves = chaves
        self.mapeamento = mapeamento

        self.nome_planilha_a = nome_planilha_a
        self.nome_planilha_b = nome_planilha_b

        self.consistentes = pd.DataFrame()
        self.exclusivos_a = pd.DataFrame()
        self.exclusivos_b = pd.DataFrame()
        self.inconsistentes = pd.DataFrame()
        self.consolidado = pd.DataFrame()

    def _criar_indice(self, df):

        return df.set_index(
            self.chaves,
            drop=False
        )

    def _localizar_exclusivos(self):

        indice_a = self._criar_indice(self.df_a)
        indice_b = self._criar_indice(self.df_b)

        chaves_a = set(indice_a.index)
        chaves_b = set(indice_b.index)

        exclusivos_a = chaves_a - chaves_b
        exclusivos_b = chaves_b - chaves_a

        if exclusivos_a:

            self.exclusivos_a = (
                indice_a
                .loc[list(exclusivos_a)]
                .reset_index(drop=True)
            )

        else:

            self.exclusivos_a = pd.DataFrame(
                columns=self.df_a.columns
            )

        if exclusivos_b:

            self.exclusivos_b = (
                indice_b
                .loc[list(exclusivos_b)]
                .reset_index(drop=True)
            )

        else:

            self.exclusivos_b = pd.DataFrame(
                columns=self.df_b.columns
            )
    def _localizar_consistentes_e_inconsistentes(self):

        indice_a = self._criar_indice(self.df_a)
        indice_b = self._criar_indice(self.df_b)

        chaves_comuns = (
            set(indice_a.index)
            .intersection(set(indice_b.index))
        )

        consistentes = []
        inconsistentes = []

        for chave in sorted(chaves_comuns):

            registro_a = indice_a.loc[chave]
            registro_b = indice_b.loc[chave]

            if isinstance(registro_a, pd.DataFrame):
                registro_a = registro_a.iloc[0]

            if isinstance(registro_b, pd.DataFrame):
                registro_b = registro_b.iloc[0]

            campos_diferentes = []

            for coluna_a, coluna_b in self.mapeamento.items():

                if coluna_b == "Não comparar":
                    continue

                valor_a = str(
                    registro_a[coluna_a]
                ).strip()

                valor_b = str(
                    registro_b[coluna_b]
                ).strip()

                if valor_a != valor_b:

                    campos_diferentes.append(
                        coluna_a
                    )

            if len(campos_diferentes) == 0:

                consistentes.append(
                    registro_a.to_dict()
                )

            else:

                motivo = "; ".join(
                    campos_diferentes
                )

                linha_a = registro_a.to_dict()
                linha_b = registro_b.to_dict()

                linha_a["Origem"] = "Planilha A"
                linha_b["Origem"] = "Planilha B"

                linha_a[
                    "Motivo da Inconsistência"
                ] = motivo

                linha_b[
                    "Motivo da Inconsistência"
                ] = motivo

                inconsistentes.append(
                    linha_a
                )

                inconsistentes.append(
                    linha_b
                )

        self.consistentes = pd.DataFrame(
            consistentes
        )

        self.inconsistentes = pd.DataFrame(
            inconsistentes
        )
    def _gerar_consolidado(self):

        tabelas = []

        if not self.consistentes.empty:
            tabelas.append(self.consistentes)

        if not self.exclusivos_a.empty:
            tabelas.append(self.exclusivos_a)

        if not self.exclusivos_b.empty:
            tabelas.append(self.exclusivos_b)

        if not self.inconsistentes.empty:
            tabelas.append(
                self.inconsistentes.drop(
                    columns=[
                        "Origem",
                        "Motivo da Inconsistência"
                    ],
                    errors="ignore"
                )
            )

        if len(tabelas) == 0:

            self.consolidado = pd.DataFrame()

            return

        self.consolidado = (
            pd.concat(
                tabelas,
                ignore_index=True
            )
            .drop_duplicates()
            .reset_index(drop=True)
        )

    def executar(self):

        self._localizar_exclusivos()

        self._localizar_consistentes_e_inconsistentes()

        self._gerar_consolidado()

        resumo = ResumoComparacao(

            nome_planilha_a=self.nome_planilha_a,
            nome_planilha_b=self.nome_planilha_b,

            total_planilha_a=len(self.df_a),
            total_planilha_b=len(self.df_b),

            consistentes=len(self.consistentes),

            exclusivos_a=len(self.exclusivos_a),

            exclusivos_b=len(self.exclusivos_b),

            inconsistentes=int(
                len(self.inconsistentes) / 2
            ),

            consolidado=len(self.consolidado)

        )

        return ResultadoComparacao(

            resumo=resumo,

            consistentes=self.consistentes,

            exclusivos_a=self.exclusivos_a,

            exclusivos_b=self.exclusivos_b,

            inconsistentes=self.inconsistentes,

            consolidado=self.consolidado

        )