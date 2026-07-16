"""Catálogo extensível de conceitos de reconciliação."""

from __future__ import annotations

from reconciliador.v2.modelos import Conceito, TipoDado


class CatalogoConceitos:
    def __init__(self, conceitos: list[Conceito] | tuple[Conceito, ...] = ()):
        self._itens = {conceito.id: conceito for conceito in conceitos}

    def obter(self, conceito_id: str) -> Conceito:
        try:
            return self._itens[conceito_id]
        except KeyError as erro:
            raise ValueError(f"Conceito desconhecido: {conceito_id!r}.") from erro

    def listar(self) -> tuple[Conceito, ...]:
        return tuple(self._itens.values())


CATALOGO_PADRAO = CatalogoConceitos(
    [
        Conceito("numero_nf", "Número da Nota Fiscal", TipoDado.IDENTIFICADOR,
                 "Identificador da nota fiscal.", ("numero_nf",)),
        Conceito("fornecedor", "Fornecedor", TipoDado.TEXTO,
                 "Razão social ou nome do fornecedor.", ("fornecedor_arquivo_nf",)),
        Conceito("valor", "Valor", TipoDado.DECIMAL,
                 "Valor monetário.", ("valor_monetario",)),
        Conceito("data_emissao", "Data de emissão", TipoDado.DATA),
        Conceito("cnpj", "CNPJ", TipoDado.DOCUMENTO),
        Conceito("cpf", "CPF", TipoDado.DOCUMENTO),
        Conceito("pedido", "Pedido", TipoDado.IDENTIFICADOR),
        Conceito("centro_custo", "Centro de custo", TipoDado.IDENTIFICADOR),
    ]
)
