from __future__ import annotations

import json
from pathlib import Path


ARQUIVO_EQUIVALENCIAS = (
    Path(__file__).parents[2]
    / "config"
    / "equivalencias.json"
)


class Aprendizado:

    def __init__(self):

        self._equivalencias = self._carregar()

    def _carregar(self):

        if not ARQUIVO_EQUIVALENCIAS.exists():
            return {}

        with open(
            ARQUIVO_EQUIVALENCIAS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)
    def salvar(self):

        with open(
            ARQUIVO_EQUIVALENCIAS,
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                self._equivalencias,
                arquivo,
                ensure_ascii=False,
                indent=4
            )
    def adicionar_equivalencia(
        self,
        conceito: str,
        valor_a: str,
        valor_b: str
    ):

        valor_a = valor_a.strip()
        valor_b = valor_b.strip()

        equivalencias = self._equivalencias.setdefault(conceito, {})

        lista = equivalencias.setdefault(valor_a, [])

        if valor_b not in lista:
            lista.append(valor_b)

        self.salvar()
    def equivalentes(
        self,
        conceito: str,
        valor_a: str,
        valor_b: str
    ) -> bool:

        valor_a = valor_a.strip()
        valor_b = valor_b.strip()

        if valor_a == valor_b:
            return True

        equivalencias = self._equivalencias.get(conceito, {})

        if valor_b in equivalencias.get(valor_a, []):
            return True

        if valor_a in equivalencias.get(valor_b, []):
            return True

        return False