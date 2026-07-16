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
# Leitura
# ===========================================

df_a = ler_planilha(arquivo_a)
df_b = ler_planilha(arquivo_b)


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

chaves = escolher_chaves(df_a)

if len(chaves) == 0:

    st.warning(
        "Selecione pelo menos uma coluna-chave."
    )

    st.stop()


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
    chaves
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
        subset=chaves,
        keep="first"
    )


st.divider()


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
# Comparação
# ===========================================

if botao_comparar():

    comparador = Comparador(

        df_a=df_a,

        df_b=df_b,

        chaves=chaves,

        mapeamento=mapeamento,

        nome_planilha_a=arquivo_a.name,

        nome_planilha_b=arquivo_b.name

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