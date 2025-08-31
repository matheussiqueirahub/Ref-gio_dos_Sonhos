from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from .models import Cliente, Quarto, Reserva
from .storage import StorageJSON
from .utils import overlaps


@dataclass
class _Estado:
    clientes: list[Cliente]
    quartos: list[Quarto]
    reservas: list[Reserva]


class GerenciadorDeReservas:
    """Fachada para operações de clientes, quartos e reservas.

    - Verifica disponibilidade
    - Cria/modifica/cancela reservas
    - Lista entidades
    - Persiste em JSON
    """

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parents[1]
        self.storage = StorageJSON(self.base_dir)
        self._estado = _Estado(
            clientes=self.storage.load_clientes(),
            quartos=self.storage.load_quartos(),
            reservas=self.storage.load_reservas(),
        )

    # --------------- Clientes ---------------
    def adicionar_cliente(self, nome: str, telefone: str | None = None, email: str | None = None) -> Cliente:
        c = Cliente(nome=nome, telefone=telefone, email=email)
        self._estado.clientes.append(c)
        self.storage.save_clientes(self._estado.clientes)
        return c

    def editar_cliente(self, id: str, nome: Optional[str] = None, telefone: Optional[str] = None, email: Optional[str] = None) -> bool:
        c = self.obter_cliente(id)
        if not c:
            return False
        if nome is not None:
            c.nome = nome
        if telefone is not None:
            c.telefone = telefone
        if email is not None:
            c.email = email
        self.storage.save_clientes(self._estado.clientes)
        return True

    def remover_cliente(self, id: str) -> bool:
        before = len(self._estado.clientes)
        self._estado.clientes = [c for c in self._estado.clientes if c.id != id]
        changed = len(self._estado.clientes) != before
        if changed:
            self.storage.save_clientes(self._estado.clientes)
        return changed

    def listar_clientes(self) -> list[Cliente]:
        return list(self._estado.clientes)

    def obter_cliente(self, id: str) -> Optional[Cliente]:
        return next((c for c in self._estado.clientes if c.id == id), None)

    # --------------- Quartos ---------------
    def listar_quartos(self) -> list[Quarto]:
        return sorted(self._estado.quartos, key=lambda q: q.numero)

    def obter_quarto(self, numero: int) -> Optional[Quarto]:
        return next((q for q in self._estado.quartos if q.numero == numero), None)

    def quarto_disponivel(self, numero: int) -> bool:
        # Disponível agora (sem considerar datas futuras), i.e., sem reserva ativa que inclua a data atual
        today = date.today()
        for r in self._estado.reservas:
            if r.ativa and r.quarto_numero == numero and (r.checkin <= today < r.checkout):
                return False
        return True

    # --------------- Reservas ---------------
    def listar_reservas(self) -> list[Reserva]:
        # Orderna por checkin
        return sorted(self._estado.reservas, key=lambda r: (r.ativa is False, r.checkin))

    def verificar_disponibilidade(self, numero_quarto: int, checkin: date, checkout: date) -> bool:
        if checkout <= checkin:
            return False
        for r in self._estado.reservas:
            if not r.ativa:
                continue
            if r.quarto_numero != numero_quarto:
                continue
            if overlaps(r.checkin, r.checkout, checkin, checkout):
                return False
        return True

    def criar_reserva(self, cliente_id: str, numero_quarto: int, checkin: date, checkout: date) -> Optional[Reserva]:
        if not self.obter_cliente(cliente_id) or not self.obter_quarto(numero_quarto):
            return None
        if not self.verificar_disponibilidade(numero_quarto, checkin, checkout):
            return None
        r = Reserva.criar(cliente_id, numero_quarto, checkin, checkout)
        self._estado.reservas.append(r)
        self.storage.save_reservas(self._estado.reservas)
        return r

    def cancelar_reserva(self, reserva_id: str) -> bool:
        r = next((x for x in self._estado.reservas if x.id == reserva_id), None)
        if not r:
            return False
        if not r.ativa:
            return True
        r.ativa = False
        self.storage.save_reservas(self._estado.reservas)
        return True

    def modificar_reserva(self, reserva_id: str, novo_checkin: date, novo_checkout: date) -> bool:
        r = next((x for x in self._estado.reservas if x.id == reserva_id), None)
        if not r or not r.ativa:
            return False
        if not self.verificar_disponibilidade(r.quarto_numero, novo_checkin, novo_checkout):
            return False
        r.checkin = novo_checkin
        r.checkout = novo_checkout
        self.storage.save_reservas(self._estado.reservas)
        return True

