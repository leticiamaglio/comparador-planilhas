# Plataforma de Reconciliação de Planilhas

Aplicativo Streamlit para reconciliar planilhas de layouts diferentes a partir de conceitos de negócio, como Número da Nota Fiscal, Fornecedor e Valor.

## Como usar

1. Inicie o aplicativo com `streamlit run app.py`.
2. Envie as planilhas A e B e informe a linha dos cabeçalhos.
3. Para cada conceito necessário, selecione a coluna correspondente em cada planilha.
4. Quando a informação estiver dentro de um texto (por exemplo, no nome de um arquivo), escolha o extrator adequado.
5. Selecione os conceitos-chave e os conceitos que devem ser comparados.
6. Clique em **Comparar Planilhas** e baixe o relatório.

O relatório mantém o valor original, o valor padronizado e o status da extração. Chaves duplicadas e registros sem chave são enviados para abas de revisão e nunca são descartados silenciosamente.

## Extensão

Para acrescentar um conceito, registre-o em `reconciliador/v2/conceitos.py`. Para uma nova regra de extração, crie uma função que devolva `ResultadoExtracao` e registre-a em `reconciliador/v2/extratores.py`. O comparador não precisa ser alterado.
