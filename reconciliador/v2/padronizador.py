"""Converte um DataFrame de layout livre em um dataset canônico."""

from __future__ import annotations

import pandas as pd

from reconciliador.v2.conceitos import CatalogoConceitos
from reconciliador.v2.extratores import RegistroExtratores
from reconciliador.v2.modelos import ConfiguracaoPadronizacao, ResultadoPadronizacao
from reconciliador.v2.normalizadores import normalizar


class Padronizador:
    def __init__(self, catalogo: CatalogoConceitos, extratores: RegistroExtratores):
        self.catalogo = catalogo
        self.extratores = extratores

    def executar(self, dados_origem: pd.DataFrame, configuracao: ConfiguracaoPadronizacao) -> ResultadoPadronizacao:
        self._validar(dados_origem, configuracao)
        saida = pd.DataFrame(index=dados_origem.index)
        saida["_origem"] = configuracao.nome_origem
        saida["_linha_origem"] = dados_origem.index + 1
        avisos: list[str] = []
        pendencias = []

        for regra in configuracao.campos:
            conceito = self.catalogo.obter(regra.conceito_id)
            bruto = dados_origem[regra.coluna_origem]
            valores, status, mensagens = [], [], []
            for indice, valor in bruto.items():
                if regra.extrator_id:

                    resultado = self.extratores.extrair(
                        regra.extrator_id,
                        valor
                    )
                    
                    valor_final = resultado.valor
                    estado = resultado.status
                    mensagem = resultado.mensagem
                else:

                    valor_final = valor
                    estado = "direto"
                    mensagem = None

                valor_normalizado = normalizar(
                    valor_final,
                    conceito.tipo
                )

                valores.append(valor_normalizado)

                status.append(estado)

                mensagens.append(mensagem)

                if estado not in ("direto", "extraido"):

                    pendencias.append({

                        "Origem": configuracao.nome_origem,

                        "Linha": indice + 1,

                        "Conceito": conceito.nome,

                        "Texto Original": valor,

                        "Valor Extraído": valor_final,

                        "Status": estado,

                        "Mensagem": mensagem

                })

            saida[conceito.id] = valores
            saida[f"_raw_{conceito.id}"] = bruto.values
            saida[f"_status_{conceito.id}"] = status
            saida[f"_mensagem_{conceito.id}"] = mensagens
            falhas = sum(estado != "direto" and estado != "extraido" for estado in status)
            if falhas:
                avisos.append(f"{conceito.nome}: {falhas} linha(s) sem extração confiável.")
        return ResultadoPadronizacao(

    dados=saida.reset_index(drop=True),

    avisos=avisos,

    pendencias_extracao=pd.DataFrame(pendencias)

)

    def _validar(self, dados_origem: pd.DataFrame, configuracao: ConfiguracaoPadronizacao) -> None:
        ids = [campo.conceito_id for campo in configuracao.campos]
        repetidos = {id_ for id_ in ids if ids.count(id_) > 1}
        if repetidos:
            raise ValueError(f"Um conceito só pode ter uma origem por configuração: {sorted(repetidos)}.")
        for campo in configuracao.campos:
            self.catalogo.obter(campo.conceito_id)
            if campo.coluna_origem not in dados_origem.columns:
                raise ValueError(f"Coluna de origem não encontrada: {campo.coluna_origem!r}.")
            if campo.extrator_id:
                self.extratores.obter(campo.extrator_id)
