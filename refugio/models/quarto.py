from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TipoQuarto(str, Enum):
    SINGLE = "Single"
    DOUBLE = "Double"
    SUITE = "Suite"


@dataclass
class Quarto:
    """Entidade Quarto do hotel."""

    numero: int
    tipo: TipoQuarto
    preco_diaria: float

    def exibir_informacoes(self) -> str:  # polimorfismo também aqui
        return f"Quarto {self.numero} | {self.tipo.value} | R$ {self.preco_diaria:.2f}"

    def to_dict(self) -> dict:
        return {"numero": self.numero, "tipo": self.tipo.value, "preco_diaria": self.preco_diaria}

    @staticmethod
    def from_dict(d: dict) -> "Quarto":
        return Quarto(numero=int(d["numero"]), tipo=TipoQuarto(d["tipo"]), preco_diaria=float(d["preco_diaria"]))

