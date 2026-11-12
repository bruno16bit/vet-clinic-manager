from __future__ import annotations
from typing import TYPE_CHECKING

from usuarios.usuario import Usuario

if TYPE_CHECKING:
    # só para tipagem, não é importado na execução
    from animais.pet import Pet


class Tutor(Usuario):
    def __init__(self, id: int, nome: str, cpf: str, telefone: str, senha: str, email: str):
        super().__init__(id, nome, cpf, telefone, senha)
        self.email = email
        # composição: os pets pertencem ao tutor e somem junto com ele
        self.__pets: list[Pet] = []

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("O e-mail deve ser um texto.")
        valor = valor.strip()
        nome_usuario, _, dominio = valor.partition("@")
        if (not nome_usuario or " " in valor or "." not in dominio
                or dominio.startswith(".") or dominio.endswith(".")):
            raise ValueError("O e-mail informado não é válido.")
        self.__email = valor.lower()

    def adicionar_pet(self, pet: Pet) -> None:
        if any(p.id == pet.id for p in self.__pets):
            raise ValueError(f"Este tutor já tem um pet com o id {pet.id}.")
        self.__pets.append(pet)

    def listar_pets(self) -> list[Pet]:
        # devolve uma cópia, para ninguém mexer na lista interna por fora
        return list(self.__pets)

    def obter_permissoes(self) -> list[str]:
        return [
            "agendar_atendimento",
            "remarcar_atendimento",
            "cancelar_atendimento",
            "consultar_historico_clinico",
        ]