"""
interface.py

Responsável pelos componentes visuais da aplicação.
"""

import streamlit as st

def aplicar_estilo():

    st.markdown("""
    <style>

    #MainMenu{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    .block-container{
        padding-top:1rem;
        padding-bottom:2rem;
        padding-left:3rem;
        padding-right:3rem;
    }

    </style>
    """, unsafe_allow_html=True)

def configurar_pagina():

    st.set_page_config(
        page_title="Comparador de Planilhas",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def mostrar_titulo():

    st.title("📊 Comparador de Planilhas")

    st.write(
    "Compare automaticamente duas planilhas com estruturas semelhantes, "
    "identificando registros consistentes, inconsistentes, exclusivos e gerando um relatório consolidado."
    )
def mostrar_sidebar():

    with st.sidebar:

        st.title("📊 Comparador de Planilhas")

        st.divider()

        with st.expander("🚀 Primeiros Passos"):

            st.markdown("""

1. Faça o upload das duas planilhas.

2. Escolha a(s) **coluna(s)-chave**.

A coluna-chave é utilizada para localizar o mesmo registro nas duas planilhas.

Ela deve identificar cada registro de forma única.

Exemplos:

- CPF
- Código do Produto
- Número da Nota Fiscal
- Pedido + Item

3. Confira o mapeamento das colunas.

4. Clique em **Comparar Planilhas**.

5. Analise os resultados e exporte o relatório em Excel.

""")
            
        with st.expander("📊 Como interpretar os resultados"):
            st.markdown("""

### 🟢 Consistentes

Registros que aparecem nas duas planilhas e possuem exatamente os mesmos valores em todas as colunas comparadas.

---

### 🟡 Inconsistentes

Registros que aparecem nas duas planilhas, mas apresentam diferenças em uma ou mais colunas comparadas.

A coluna **Motivo da Inconsistência** informa quais campos possuem divergências.

---

### 🔵 Exclusivos da Planilha A

Registros encontrados apenas na primeira planilha.

---

### 🟣 Exclusivos da Planilha B

Registros encontrados apenas na segunda planilha.

---

### ⚪ Consolidado

Reúne todos os registros das duas planilhas, eliminando duplicidades conforme a chave selecionada.

""")

        with st.expander("ℹ️ Sobre"):

            st.markdown("""

**Comparador de Planilhas**

Versão **1.1.0**

Desenvolvido por **Letícia Maglio**

Ferramenta desenvolvida para comparar duas planilhas, identificar divergências e gerar um relatório consolidado.

""")

        st.divider()

        st.caption("© 2026 • Comparador de Planilhas")

        
def upload_planilhas():

    st.subheader("📂 Upload das Planilhas")

    col1, col2 = st.columns(2)

    with col1:

        arquivo_a = st.file_uploader(
            "Planilha A",
            type=["xlsx", "xls", "csv"]
        )

    with col2:

        arquivo_b = st.file_uploader(
            "Planilha B",
            type=["xlsx", "xls", "csv"]
        )

    return arquivo_a, arquivo_b


def mostrar_preview(df_a, df_b):

    st.subheader("👀 Pré-visualização")

    aba_a, aba_b = st.tabs(
        [
            "Planilha A",
            "Planilha B"
        ]
    )

    with aba_a:

        st.dataframe(
            df_a,
            use_container_width=True,
            height=300
        )

    with aba_b:

        st.dataframe(
            df_b,
            use_container_width=True,
            height=300
        )

def mostrar_dashboard(
    resultado,
    chaves
):

    st.subheader("📊 Resumo da Comparação")

    total = max(resultado.resumo.consolidado, 1)

    pct_consistentes = resultado.resumo.consistentes / total * 100
    pct_inconsistentes = resultado.resumo.inconsistentes / total * 100
    pct_exclusivos_a = resultado.resumo.exclusivos_a / total * 100
    pct_exclusivos_b = resultado.resumo.exclusivos_b / total * 100

    st.caption(
        f"**Planilha A:** {resultado.resumo.nome_planilha_a} | "
        f"**Planilha B:** {resultado.resumo.nome_planilha_b}"
    )

    st.caption(
        f"**🔑 Chave utilizada:** {' + '.join(chaves)}"
    )

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "🟢 Consistentes",
            f"{resultado.resumo.consistentes} registros"
        )

        st.progress(pct_consistentes / 100)

        st.caption(f"{pct_consistentes:.1f}% do total")

        st.metric(
            "🟡 Inconsistentes",
            f"{resultado.resumo.inconsistentes} registros"
        )

        st.progress(pct_inconsistentes / 100)

        st.caption(f"{pct_inconsistentes:.1f}% do total")

    with c2:

        st.metric(
            "🔵 Exclusivos da Planilha A",
            f"{resultado.resumo.exclusivos_a} registros"
        )

        st.progress(pct_exclusivos_a / 100)

        st.caption(f"{pct_exclusivos_a:.1f}% do total")

        st.metric(
            "🟣 Exclusivos da Planilha B",
            f"{resultado.resumo.exclusivos_b} registros"
        )

        st.progress(pct_exclusivos_b / 100)

        st.caption(f"{pct_exclusivos_b:.1f}% do total")

    st.metric(
        "⚪ Total Consolidado",
        f"{resultado.resumo.consolidado} registros"
    )

    st.success("✅ Comparação concluída com sucesso")

    st.divider()
        # ==========================================================
    # Resumo da Análise
    # ==========================================================

    st.subheader("📋 Resumo da Análise")

    mensagens = []

    if resultado.resumo.inconsistentes == 0:
        mensagens.append(
            "✅ Nenhuma inconsistência foi encontrada entre os registros comparados."
        )
    else:
        mensagens.append(
            f"⚠ Foram encontradas {resultado.resumo.inconsistentes} inconsistências que precisam ser analisadas."
        )

    if resultado.resumo.exclusivos_a > 0:
        mensagens.append(
            f"🔵 Existem {resultado.resumo.exclusivos_a} registros exclusivos na Planilha A."
        )

    if resultado.resumo.exclusivos_b > 0:
        mensagens.append(
            f"🟣 Existem {resultado.resumo.exclusivos_b} registros exclusivos na Planilha B."
        )

    mensagens.append(
        f"⚪ O consolidado possui {resultado.resumo.consolidado} registros."
    )

    for mensagem in mensagens:
        st.write(mensagem)

    st.divider()
        # ==========================================================
    # Parecer da Comparação
    # ==========================================================

    st.subheader("📌 Parecer da Comparação")

    if (
        resultado.resumo.inconsistentes == 0
        and resultado.resumo.exclusivos_a == 0
        and resultado.resumo.exclusivos_b == 0
    ):

        st.success(
            """
As duas planilhas possuem exatamente os mesmos registros para a chave utilizada.

Nenhuma inconsistência ou registro exclusivo foi encontrado.
"""
        )

    elif resultado.resumo.inconsistentes == 0:

        st.info(
            f"""
Não foram encontradas inconsistências entre os registros comparados.

Foram identificados:

• {resultado.resumo.exclusivos_a} registros exclusivos na Planilha A.

• {resultado.resumo.exclusivos_b} registros exclusivos na Planilha B.

Esse comportamento costuma ser esperado quando as planilhas representam períodos diferentes ou bases distintas.

Consulte as abas **Exclusivos A** e **Exclusivos B** para analisar esses registros.
"""
        )

    else:

        percentual = (
            resultado.resumo.inconsistentes
            / total
        ) * 100

        if percentual < 10:

            st.warning(
                f"""
Foram encontradas {resultado.resumo.inconsistentes} inconsistências.

A quantidade de divergências é relativamente pequena, porém recomenda-se revisar a aba **Inconsistentes** antes da utilização dos dados.
"""
            )

        elif percentual < 25:

            st.warning(
                f"""
Foram encontradas {resultado.resumo.inconsistentes} inconsistências.

A quantidade de divergências merece atenção.

Recomenda-se revisar cuidadosamente a aba **Inconsistentes** antes de utilizar a base consolidada.
"""
            )

        else:

            st.error(
                f"""
Foram encontradas {resultado.resumo.inconsistentes} inconsistências.

A proporção de divergências é elevada ({percentual:.1f}% dos registros).

Recomenda-se revisar os critérios de comparação e validar os dados de origem antes de utilizar o resultado.
"""
            )

def mostrar_resultados(resultado):

    abas = st.tabs([
        "🟢 Consistentes",
        "🔵 Exclusivos A",
        "🟣 Exclusivos B",
        "🟡 Inconsistentes",
        "⚪ Consolidado"
    ])

    with abas[0]:

        st.dataframe(
            resultado.consistentes,
            use_container_width=True
        )

    with abas[1]:

        st.dataframe(
            resultado.exclusivos_a,
            use_container_width=True
        )

    with abas[2]:

        st.dataframe(
            resultado.exclusivos_b,
            use_container_width=True
        )

    with abas[3]:

        st.dataframe(
            resultado.inconsistentes,
            use_container_width=True
        )

    with abas[4]:

        st.dataframe(
            resultado.consolidado,
            use_container_width=True
        )


def botao_comparar():

    return st.button(
        "🚀 Comparar Planilhas",
        use_container_width=True
    )


def botao_download(arquivo_excel):

    st.download_button(
        label="📥 Baixar Relatório Excel",
        data=arquivo_excel,
        file_name="Relatorio_Reconciliacao.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )