from __future__ import annotations
from typing import TYPE_CHECKING

from usuarios.usuario import Usuario

if TYPE_CHECKING:
    # só para tipagem, não é importado na execução (evita import circular)
    from atendimentos.atendimento import Atendimento
    from atendimentos.prontuario import Prontuario


class Veterinario(Usuario):
    def __init__(self, id: int, nome: str, cpf: str, telefone: str, senha: str,
                 crmv: str, especialidade: str):
        super().__init__(id, nome, cpf, telefone, senha)
        self.crmv = crmv
        self.especialidade = especialidade

    @property
    def crmv(self) -> str:
        return self.__crmv

    @crmv.setter
    def crmv(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O CRMV não pode ser vazio.")
        self.__crmv = valor.strip().upper()

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("A especialidade não pode ser vazia.")
        self.__especialidade = valor.strip()

    def registrar_prontuario(self, atendimento: Atendimento, texto: str,
                             prescricao: str = "") -> Prontuario:
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("O texto do prontuário não pode ser vazio.")
        # quem cria e guarda o prontuário é o próprio atendimento (composição)
        return atendimento.criar_prontuario(texto.strip(), (prescricao or "").strip())

    def obter_permissoes(self) -> list[str]:
        return ["registrar_prontuario", "consultar_historico_clinico"]