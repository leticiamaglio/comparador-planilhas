"""Componentes Streamlit da configuração de conceitos."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from reconciliador.v2.conceitos import CatalogoConceitos
from reconciliador.v2.modelos import ConfiguracaoPadronizacao, EspecificacaoReconciliacao, RegraCampo


NAO_USAR = "— Não usar —"
SEM_EXTRACAO = "Valor direto (sem extração)"


def mostrar_mapeamento_conceitos(
    dados_a: pd.DataFrame, dados_b: pd.DataFrame, catalogo: CatalogoConceitos
) -> tuple[ConfiguracaoPadronizacao, ConfiguracaoPadronizacao, EspecificacaoReconciliacao]:
    st.subheader("Mapeamento de conceitos")
    st.caption("Indique de onde cada informação vem. A mesma coluna pode alimentar mais de um conceito.")
    regras_a, regras_b, comuns = [], [], []
    for conceito in catalogo.listar():
        with st.expander(conceito.nome, expanded=conceito.id in {"numero_nf", "valor", "fornecedor"}):
            coluna_a, coluna_b = st.columns(2)
            with coluna_a:
                escolha_a = st.selectbox("Planilha A", [NAO_USAR, *dados_a.columns], key=f"v2_a_{conceito.id}")
                extrator_a = _escolher_extrator(conceito, "a") if escolha_a != NAO_USAR else None
            with coluna_b:
                escolha_b = st.selectbox("Planilha B", [NAO_USAR, *dados_b.columns], key=f"v2_b_{conceito.id}")
                extrator_b = _escolher_extrator(conceito, "b") if escolha_b != NAO_USAR else None
            if escolha_a != NAO_USAR:
                regras_a.append(RegraCampo(conceito.id, escolha_a, extrator_a))
            if escolha_b != NAO_USAR:
                regras_b.append(RegraCampo(conceito.id, escolha_b, extrator_b))
            if escolha_a != NAO_USAR and escolha_b != NAO_USAR:
                comuns.append(conceito)

    if not comuns:
        st.warning("Mapeie ao menos um mesmo conceito nas duas planilhas para continuar.")
        return ConfiguracaoPadronizacao("Planilha A", tuple(regras_a)), ConfiguracaoPadronizacao("Planilha B", tuple(regras_b)), EspecificacaoReconciliacao((), ())
    opcoes = {conceito.nome: conceito.id for conceito in comuns}
    chaves_nomes = st.multiselect("Conceitos-chave", list(opcoes), default=[next(iter(opcoes))],
                                  help="A combinação destes conceitos deve identificar um registro.")
    campos_nomes = st.multiselect("Conceitos a comparar", list(opcoes), default=list(opcoes),
                                  help="Campos diferentes serão apontados como inconsistência.")
    return (
        ConfiguracaoPadronizacao("Planilha A", tuple(regras_a)),
        ConfiguracaoPadronizacao("Planilha B", tuple(regras_b)),
        EspecificacaoReconciliacao(tuple(opcoes[nome] for nome in chaves_nomes), tuple(opcoes[nome] for nome in campos_nomes)),
    )


def _escolher_extrator(conceito, lado: str) -> str | None:
    opcoes = [SEM_EXTRACAO, *conceito.extratores_compativeis]
    escolha = st.selectbox("Como obter o valor", opcoes, key=f"v2_extrator_{lado}_{conceito.id}")
    return None if escolha == SEM_EXTRACAO else escolha
