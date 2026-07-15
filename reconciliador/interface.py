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
        page_title="Reconciliador Inteligente de Planilhas",
        page_icon="📊",
        layout="wide"
    )


def mostrar_titulo():

    st.title("📊 Reconciliador Inteligente de Planilhas")

    st.write(
        "Compare duas planilhas e identifique automaticamente "
        "registros consistentes, exclusivos e inconsistentes."
    )


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

    st.subheader("📊 Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🟢 Consistentes",
            resultado.resumo.consistentes
        )

        st.metric(
            "🔵 Exclusivos A",
            resultado.resumo.exclusivos_a
        )

    with c2:

        st.metric(
            "🟣 Exclusivos B",
            resultado.resumo.exclusivos_b
        )

        st.metric(
            "🟡 Inconsistentes",
            resultado.resumo.inconsistentes
        )

    with c3:

        st.metric(
            "⚪ Consolidado",
            resultado.resumo.consolidado
        )

    st.markdown("---")


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