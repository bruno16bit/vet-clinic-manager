from __future__ import annotations
from typing import TYPE_CHECKING

from usuarios.usuario import Usuario

if TYPE_CHECKING:
    # só para tipagem; ajusta os caminhos conforme a estrutura do projeto
    from usuarios.tutor import Tutor
    from animais.pet import Pet
    from atendimentos.atendimento import Atendimento
    from clinica.clinica import Clinica


class Recepcionista(Usuario):
    def __init__(self, id: int, nome: str, cpf: str, telefone: str, senha: str, turno: str):
        super().__init__(id, nome, cpf, telefone, senha)
        self.turno = turno

    @property
    def turno(self) -> str:
        return self.__turno

    @turno.setter
    def turno(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O turno não pode ser vazio.")
        self.__turno = valor.strip()

    def cadastrar_tutor(self, tutor: Tutor, clinica: Clinica) -> None:
        clinica.adicionar_tutor(tutor)

    def cadastrar_pet(self, tutor: Tutor, pet: Pet) -> None:
        tutor.adicionar_pet(pet)

    def atualizar_tutor(self, tutor: Tutor, nome: str = None,
                        telefone: str = None, email: str = None) -> None:
        # os setters do tutor é que validam os valores novos
        if nome is not None:
            tutor.nome = nome
        if telefone is not None:
            tutor.telefone = telefone
        if email is not None:
            tutor.email = email

    def excluir_tutor(self, tutor: Tutor, clinica: Clinica) -> None:
        # os pets são excluídos junto, porque pertencem ao tutor (composição)
        clinica.remover_tutor(tutor)

    def agendar_atendimento(self, atendimento: Atendimento, clinica: Clinica) -> bool:
        return clinica.agendar(atendimento, solicitante=self)

    def obter_permissoes(self) -> list[str]:
        return [
            "cadastrar_tutor_e_pet",
            "atualizar_cadastro",
            "excluir_cadastro",
            "agendar_atendimento",
            "remarcar_atendimento",
            "cancelar_atendimento",
        ]