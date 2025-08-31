from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from uuid import uuid4


@dataclass
class Reserva:
    """Reserva de um quarto para um cliente."""

    id: str
    cliente_id: str
    quarto_numero: int
    checkin: date
    checkout: date
    ativa: bool = True

    @staticmethod
    def criar(cliente_id: str, quarto_numero: int, checkin: date, checkout: date) -> "Reserva":
        return Reserva(id=str(uuid4()), cliente_id=cliente_id, quarto_numero=quarto_numero, checkin=checkin, checkout=checkout, ativa=True)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "quarto_numero": self.quarto_numero,
            "checkin": self.checkin.isoformat(),
            "checkout": self.checkout.isoformat(),
            "ativa": self.ativa,
        }

    @staticmethod
    def from_dict(d: dict) -> "Reserva":
        from datetime import date

        return Reserva(
            id=d["id"],
            cliente_id=d["cliente_id"],
            quarto_numero=int(d["quarto_numero"]),
            checkin=date.fromisoformat(d["checkin"]),
            checkout=date.fromisoformat(d["checkout"]),
            ativa=bool(d.get("ativa", True)),
        )

