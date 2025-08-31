from __future__ import annotations

from uuid import uuid4

from .pessoa import Pessoa


class Cliente(Pessoa):
    """Cliente do hotel. Herda de Pessoa e adiciona ID único.

    Demonstra herança e polimorfismo (exibir_informacoes sobrescrito).
    """

    def __init__(self, nome: str, telefone: str | None = None, email: str | None = None, id: str | None = None):
        super().__init__(nome, telefone, email)
        self.__id = id or str(uuid4())

    @property
    def id(self) -> str:
        return self.__id

    def exibir_informacoes(self) -> str:
        base = f"Cliente: {self.nome}"
        if self.email:
            base += f" | Email: {self.email}"
        if self.telefone:
            base += f" | Tel: {self.telefone}"
        base += f" | ID: {self.id}"
        return base

    # Serialização simples p/ persistência JSON
    def to_dict(self) -> dict:
        return {"id": self.id, "nome": self.nome, "telefone": self.telefone, "email": self.email}

    @staticmethod
    def from_dict(d: dict) -> "Cliente":
        return Cliente(id=d.get("id"), nome=d.get("nome", ""), telefone=d.get("telefone"), email=d.get("email"))

