from __future__ import annotations
from typing import TYPE_CHECKING

from usuarios.recepcionista import Recepcionista
from clinica.status_atendimento import StatusAtendimento

if TYPE_CHECKING:
    # só para tipagem; ajusta os caminhos conforme a estrutura do projeto
    from clinica.servico import Servico
    from clinica.clinica import Clinica


class Administrador(Recepcionista):
    def __init__(self, id: int, nome: str, cpf: str, telefone: str, senha: str,
                 turno: str, nivel_acesso: int):
        super().__init__(id, nome, cpf, telefone, senha, turno)
        self.nivel_acesso = nivel_acesso

    @property
    def nivel_acesso(self) -> int:
        return self.__nivel_acesso

    @nivel_acesso.setter
    def nivel_acesso(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("O nível de acesso deve ser um número inteiro positivo.")
        self.__nivel_acesso = valor

    def cadastrar_servico(self, servico: Servico, clinica: Clinica) -> None:
        clinica.adicionar_servico(servico)

    def gerenciar_precos(self, servico: Servico, novo_preco: float) -> None:
        # o setter do Servico é que valida o preço (não aceita valor negativo)
        servico.preco = novo_preco

    def excluir_servico(self, servico: Servico, clinica: Clinica) -> None:
        clinica.remover_servico(servico)

    def emitir_relatorio(self, clinica: Clinica) -> str:
        atendimentos = clinica.listar_atendimentos()
        por_status = {status: 0 for status in StatusAtendimento}
        faturamento = 0.0

        for atendimento in atendimentos:
            por_status[atendimento.status] += 1
            # só conta no faturamento o que já foi concluído
            if atendimento.status == StatusAtendimento.CONCLUIDO:
                faturamento += atendimento.calcular_custo()

        linhas = [
            "=== Relatório Financeiro e de Atendimentos ===",
            f"Total de atendimentos: {len(atendimentos)}",
        ]
        for status, quantidade in por_status.items():
            linhas.append(f"  {status.name.capitalize()}: {quantidade}")
        linhas.append(f"Faturamento (concluídos): R$ {faturamento:.2f}")
        return "\n".join(linhas)

    def obter_permissoes(self) -> list[str]:
        # tudo o que a recepcionista faz, mais as permissões financeiras
        return super().obter_permissoes() + [
            "cadastrar_servico",
            "atualizar_servico",
            "excluir_servico",
            "emitir_relatorio",
        ]