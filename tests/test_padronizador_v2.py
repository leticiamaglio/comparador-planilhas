import unittest

import pandas as pd

from reconciliador.exportador import gerar_excel
from reconciliador.v2 import CATALOGO_PADRAO, ConfiguracaoPadronizacao, Padronizador, RegraCampo
from reconciliador.v2.extratores import EXTRATORES_PADRAO
from reconciliador.v2.modelos import EspecificacaoReconciliacao
from reconciliador.v2.reconciliador import Reconciliador


class PadronizadorV2Test(unittest.TestCase):
    def test_extrai_e_padroniza_campos_de_uma_mesma_coluna(self):
        origem = pd.DataFrame({"Nome do Arquivo": ["NF 104642 HOTEL DAN R$288,40.pdf"]})
        configuracao = ConfiguracaoPadronizacao(
            nome_origem="Planilha A",
            campos=(
                RegraCampo("numero_nf", "Nome do Arquivo", "numero_nf"),
                RegraCampo("valor", "Nome do Arquivo", "valor_monetario"),
                RegraCampo("fornecedor", "Nome do Arquivo", "fornecedor_arquivo_nf"),
            ),
        )

        resultado = Padronizador(CATALOGO_PADRAO, EXTRATORES_PADRAO).executar(origem, configuracao)

        self.assertEqual(resultado.dados.loc[0, "numero_nf"], "104642")
        self.assertEqual(str(resultado.dados.loc[0, "valor"]), "288.40")
        self.assertEqual(resultado.dados.loc[0, "fornecedor"], "hotel dan")

    def test_reconciliador_compara_modelos_canonicos_e_isola_duplicidades(self):
        dados_a = pd.DataFrame({"_origem": ["A", "A", "A"], "numero_nf": ["1", "2", "2"], "valor": [10, 20, 20]})
        dados_b = pd.DataFrame({"_origem": ["B", "B"], "numero_nf": ["1", "3"], "valor": [10, 30]})
        resultado = Reconciliador().executar(
            dados_a,
            dados_b,
            EspecificacaoReconciliacao(("numero_nf",), ("valor",)),
        )
        self.assertEqual(resultado.resumo.consistentes, 1)
        self.assertEqual(resultado.resumo.exclusivos_b, 1)
        self.assertEqual(resultado.resumo.duplicados_a, 2)
        arquivo = gerar_excel(resultado)
        self.assertGreater(len(arquivo.getvalue()), 0)


if __name__ == "__main__":
    unittest.main()
