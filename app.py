from reconciliador.configuracoes import (
    mostrar_opcoes
)
from reconciliador.interface import (
    configurar_pagina,
    aplicar_estilo,
    mostrar_titulo,
    mostrar_sidebar,
    upload_planilhas,
    mostrar_preview,
    mostrar_dashboard,
    mostrar_resultados,
    botao_comparar,
    botao_download
)

from reconciliador.leitor import (
    ler_planilha
)

from reconciliador.chave import (
    escolher_chaves,
    validar_chaves,
    montar_mapeamento
)

from reconciliador.comparador import (
    Comparador
)

from reconciliador.exportador import (
    gerar_excel
)

import streamlit as st


# ===========================================
# Configuração
# ===========================================

configurar_pagina()
aplicar_estilo()

mostrar_titulo()
mostrar_sidebar()


# ===========================================
# Upload
# ===========================================

arquivo_a, arquivo_b = upload_planilhas()

if arquivo_a is None or arquivo_b is None:
    st.stop()

# ===========================================
# Configuração da leitura
# ===========================================

st.subheader("⚙️ Configuração da leitura")

col1, col2 = st.columns(2)

with col1:

    cabecalho_a = st.number_input(
        "Cabeçalho da Planilha A começa na linha:",
        min_value=1,
        value=1,
        step=1
    )

with col2:

    cabecalho_b = st.number_input(
        "Cabeçalho da Planilha B começa na linha:",
        min_value=1,
        value=1,
        step=1
    )

# ===========================================
# Leitura
# ===========================================

try:

    df_a = ler_planilha(
        arquivo_a,
        cabecalho=cabecalho_a - 1
    )

    df_b = ler_planilha(
        arquivo_b,
        cabecalho=cabecalho_b - 1
    )

except Exception as erro:

    st.error("❌ Não foi possível abrir uma das planilhas.")

    st.exception(erro)

    st.stop()

# ===========================================
# Pré-visualização
# ===========================================

mostrar_preview(
    df_a,
    df_b
)

st.divider()


# ===========================================
# Escolha das chaves
# ===========================================

chave_a, chave_b = escolher_chaves(
    df_a,
    df_b
)

chaves = [chave_a]


# ===========================================
# Validação das chaves
# ===========================================

valida_a, duplicados_a = validar_chaves(
    df_a,
    chaves
)

if not valida_a:

    st.warning(
        f"⚠️ Foram encontrados {len(duplicados_a)} registros duplicados na Planilha A. "
        "Eles serão desconsiderados da comparação."
    )

    st.dataframe(
        duplicados_a,
        use_container_width=True
    )

    df_a = df_a.drop_duplicates(
        subset=chaves,
        keep="first"
    )


valida_b, duplicados_b = validar_chaves(
    df_b,
    [chave_b]
)

if not valida_b:

    st.warning(
        f"⚠️ Foram encontrados {len(duplicados_b)} registros duplicados na Planilha B. "
        "Eles serão desconsiderados da comparação."
    )

    st.dataframe(
        duplicados_b,
        use_container_width=True
    )

    df_b = df_b.drop_duplicates(
    subset=[chave_b],
    keep="first"
)


st.divider()

if chave_a != chave_b:

    df_b = df_b.rename(
        columns={
            chave_b: chave_a
        }
    )

# ===========================================
# Mapeamento
# ===========================================

mapeamento = montar_mapeamento(
    df_a,
    df_b,
    chaves
)

st.divider()

# ===========================================
# Opções Avançadas
# ===========================================

opcoes = mostrar_opcoes()

# ===========================================
# Comparação
# ===========================================

if botao_comparar():

    comparador = Comparador(

    df_a=df_a,

    df_b=df_b,

    chaves=chaves,

    mapeamento=mapeamento,

    nome_planilha_a=arquivo_a.name,

    nome_planilha_b=arquivo_b.name,

    opcoes=opcoes

)

    resultado = comparador.executar()

    st.divider()

    mostrar_dashboard(
    resultado,
    chaves
)

    mostrar_resultados(resultado)

    st.divider()

    arquivo_excel = gerar_excel(
        resultado
    )

    botao_download(
        arquivo_excel
    )