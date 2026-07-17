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

        
def mostrar_sidebar_v2():
    """Orientacoes da interface orientada a conceitos."""
    with st.sidebar:
        st.title("Plataforma de Reconciliacao")
        st.divider()
        with st.expander("Primeiros passos", expanded=True):
            st.markdown("""
1. Envie as planilhas A e B.
2. Informe a linha em que o cabecalho inicia em cada arquivo.
3. Em **Mapeamento de conceitos**, indique em qual coluna esta cada informacao.
4. Se a informacao estiver dentro de um texto, escolha um extrator. Por exemplo, NF, fornecedor e valor podem ser extraidos de um nome de arquivo.
5. Selecione os **conceitos-chave** que identificam um registro. Voce pode combinar conceitos, como Pedido + Item.
6. Selecione os conceitos que devem ser comparados.
7. Clique em **Comparar Planilhas**, revise as abas e exporte o relatorio.

O sistema preserva o texto original, o valor padronizado e o status de cada extracao para auditoria.
""")
        with st.expander("Como interpretar os resultados", expanded=True):
            st.markdown("""
### Consistentes
Registros encontrados nas duas planilhas, com os mesmos valores nos conceitos selecionados para comparacao.

### Inconsistentes
Registros encontrados nas duas planilhas com diferenca em um ou mais conceitos. A coluna **Motivo da Inconsistencia** identifica quais conceitos divergem.

### Exclusivos A e B
Registros com chave valida encontrados apenas em uma das planilhas.

### Duplicados A e B
Registros com a mesma chave mais de uma vez na mesma planilha. Eles nao sao descartados nem comparados automaticamente, pois a correspondencia seria ambigua.

### Sem chave A e B
Registros sem valor em pelo menos um conceito-chave. Revise a origem, o mapeamento ou o extrator antes de reconciliar novamente.

### Consolidado
Reune registros consistentes e exclusivos que puderam ser reconciliados com seguranca.

### Auditoria da extracao
Colunas iniciadas por `_raw_` guardam o texto original. Colunas `_status_` indicam se o valor foi lido diretamente, extraido, se houve falha ou ambiguidade.
""")
        with st.expander("Sobre"):
            st.markdown("""
**Plataforma de Reconciliacao de Planilhas**

Versao **2.0.0**

Compare planilhas de layouts diferentes usando conceitos de negocio, sem regras especificas por cliente.
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

def mostrar_dashboard_v2(resultado, chaves):
    """Resumo da reconciliação canônica, incluindo itens que exigem revisão."""

    resumo = resultado.resumo

    st.subheader("Resultado da reconciliação")

    st.caption(
        f"**Planilha A:** {resumo.nome_planilha_a} | "
        f"**Planilha B:** {resumo.nome_planilha_b}"
    )

    st.caption(
        f"**Conceitos-chave:** {' + '.join(chaves)}"
    )

    colunas = st.columns(4)

    colunas[0].metric(
        "✅ Correspondências",
        resumo.consistentes
    )

    colunas[1].metric(
        "⚠️ Diferenças",
        resumo.inconsistentes
    )

    colunas[2].metric(
        "📄 Apenas na A",
        resumo.exclusivos_a
    )

    colunas[3].metric(
        "📄 Apenas na B",
        resumo.exclusivos_b
    )

    colunas = st.columns(2)

    colunas[0].metric(
        "🔁 Duplicados",
        resumo.duplicados_a + resumo.duplicados_b
    )

    colunas[1].metric(
        "⚠️ Não comparados",
        resumo.sem_chave_a + resumo.sem_chave_b
    )

    pendencias = []

    if resumo.inconsistentes:
        pendencias.append(f"- **{resumo.inconsistentes}** inconsistência(s)")

    if resumo.exclusivos_a:
        pendencias.append(
            f"- **{resumo.exclusivos_a}** registro(s) exclusivo(s) na Planilha A"
        )

    if resumo.exclusivos_b:
        pendencias.append(
            f"- **{resumo.exclusivos_b}** registro(s) exclusivo(s) na Planilha B"
        )

    if resumo.duplicados_a:
        pendencias.append(
            f"- **{resumo.duplicados_a}** duplicidade(s) na Planilha A"
        )

    if resumo.duplicados_b:
        pendencias.append(
            f"- **{resumo.duplicados_b}** duplicidade(s) na Planilha B"
        )

    if resumo.sem_chave_a or resumo.sem_chave_b:
        pendencias.append(
            f"- **{resumo.sem_chave_a + resumo.sem_chave_b}** registro(s) sem chave"
        )

    # Caso 1: nenhuma conciliação
    if resumo.consistentes == 0:

        st.warning(
            """
### ⚠️ Nenhum registro foi conciliado automaticamente

Verifique se:

- os conceitos-chave selecionados identificam corretamente os registros;
- as duas planilhas possuem dados correspondentes;
- os conceitos foram mapeados corretamente.
"""
        )

    # Caso 2: existem pendências
    elif pendencias:

        mensagem = (
            "### ⚠️ Atenção\n\n"
            "A conciliação foi concluída, mas alguns registros exigem análise manual.\n\n"
            + "\n".join(pendencias)
        )

        st.warning(mensagem)

    # Caso 3: tudo conciliado
    else:

        st.success(
            "✅ Todos os registros foram reconciliados automaticamente."
        )

def mostrar_resultados_v2(resultado):
    st.info("""
**Como interpretar os resultados**

✅ **Correspondências** → registros encontrados nas duas planilhas e considerados iguais.

⚠️ **Diferenças encontradas** → registros encontrados nas duas planilhas, mas com alguma informação diferente.

📄 **Apenas na Planilha A/B** → registros existentes em apenas uma das planilhas.

🔁 **Duplicados** → mais de um registro possui a mesma chave de comparação.

⚠️ **Não comparados** → faltam informações necessárias para realizar a comparação.
""")

    abas_info = []

    if not resultado.consistentes.empty:
        abas_info.append(("✅ Correspondências", resultado.consistentes))

    if not resultado.inconsistentes.empty:
        abas_info.append(("⚠️ Diferenças encontradas", resultado.inconsistentes))

    if not resultado.exclusivos_a.empty:
        abas_info.append(("📄 Apenas na Planilha A", resultado.exclusivos_a))

    if not resultado.exclusivos_b.empty:
        abas_info.append(("📄 Apenas na Planilha B", resultado.exclusivos_b))

    if not resultado.duplicados_a.empty:
        abas_info.append(("🔁 Duplicados (Planilha A)", resultado.duplicados_a))

    if not resultado.duplicados_b.empty:
        abas_info.append(("🔁 Duplicados (Planilha B)", resultado.duplicados_b))

    if not resultado.sem_chave_a.empty:
        abas_info.append(("⚠️ Não comparados (Planilha A)", resultado.sem_chave_a))

    if not resultado.sem_chave_b.empty:
        abas_info.append(("⚠️ Não comparados (Planilha B)", resultado.sem_chave_b))

    # Sempre mostra o relatório completo
    abas_info.append(("📊 Relatório completo", resultado.consolidado))

    abas = st.tabs([titulo for titulo, _ in abas_info])

    for aba, (titulo, dataframe) in zip(abas, abas_info):
        with aba:

            st.write(f"### {titulo}")

            dataframe = dataframe.drop(
                columns=["_chave_reconciliacao"],
                errors="ignore",
            )

            st.write(f"Renderizando: {titulo}")

            st.write(dataframe.dtypes)

            st.dataframe(
                dataframe,
                use_container_width=True,
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
