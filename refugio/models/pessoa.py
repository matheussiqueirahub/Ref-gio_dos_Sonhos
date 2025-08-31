from __future__ import annotations

from abc import ABC, abstractmethod


class Pessoa(ABC):
    """Classe base para entidades do tipo pessoa.

    Encapsula atributos comuns e define uma interface polimórfica
    para exibição de informações.
    """

    def __init__(self, nome: str, telefone: str | None = None, email: str | None = None):
        self.__nome = nome
        self.__telefone = telefone
        self.__email = email

    # Encapsulamento com propriedades
    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("Nome não pode ser vazio")
        self.__nome = valor.strip()

    @property
    def telefone(self) -> str | None:
        return self.__telefone

    @telefone.setter
    def telefone(self, valor: str | None) -> None:
        self.__telefone = (valor or None)

    @property
    def email(self) -> str | None:
        return self.__email

    @email.setter
    def email(self, valor: str | None) -> None:
        self.__email = (valor or None)

    @abstractmethod
    def exibir_informacoes(self) -> str:
        """Retorna uma string com informações formatadas da pessoa."""
        raise NotImplementedError

