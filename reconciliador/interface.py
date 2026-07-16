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

    header{
        visibility:hidden;
    }

    .block-container{
        padding-top:2rem;
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
        layout="wide"
    )


def mostrar_titulo():

    st.title("📊 Comparador de Planilhas")

    st.write(
    "Compare automaticamente duas planilhas com estruturas semelhantes, "
    "identificando registros consistentes, inconsistentes, exclusivos e gerando um relatório consolidado."
    )

def mostrar_ajuda():

    with st.expander("ℹ️ Como interpretar os resultados"):

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

---

### 🔑 Coluna-chave

É a coluna (ou conjunto de colunas) utilizada para identificar um registro de forma única entre as duas planilhas.

""")
        
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


def mostrar_dashboard(resultado):

    st.subheader("📊 Resumo da Comparação")

    total = max(resultado.resumo.consolidado, 1)

    pct_consistentes = resultado.resumo.consistentes / total * 100
    pct_exclusivos_a = resultado.resumo.exclusivos_a / total * 100
    pct_exclusivos_b = resultado.resumo.exclusivos_b / total * 100
    pct_inconsistentes = resultado.resumo.inconsistentes / total * 100

    st.caption(
        f"**Planilha A:** {resultado.resumo.nome_planilha_a} | "
        f"**Planilha B:** {resultado.resumo.nome_planilha_b}"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🟢 Consistentes",
            resultado.resumo.consistentes,
            f"{pct_consistentes:.1f}%"
        )

        st.metric(
            "🔵 Exclusivos A",
            resultado.resumo.exclusivos_a,
            f"{pct_exclusivos_a:.1f}%"
        )

    with c2:

        st.metric(
            "🟣 Exclusivos B",
            resultado.resumo.exclusivos_b,
            f"{pct_exclusivos_b:.1f}%"
        )

        st.metric(
            "🟡 Inconsistentes",
            resultado.resumo.inconsistentes,
            f"{pct_inconsistentes:.1f}%"
        )

    with c3:

        st.metric(
            "⚪ Consolidado",
            resultado.resumo.consolidado
        )

        st.success("✅ Comparação concluída")

    st.divider()


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