from __future__ import annotations
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from atendimentos.status_atendimento import StatusAtendimento
from usuarios.tutor import Tutor

if TYPE_CHECKING:
    # só para tipagem, não é importado na execução (evita import circular)
    from animais.pet import Pet
    from atendimentos.atendimento import Atendimento
    from clinica.servico import Servico
    from usuarios.usuario import Usuario
    from usuarios.veterinario import Veterinario

# RN04: antecedência mínima para remarcar ou cancelar
ANTECEDENCIA_MINIMA = timedelta(hours=24)


class Clinica:
    def __init__(self, nome: str):
        self.nome = nome
        # agregação: a clínica reúne esses objetos, mas eles existem por conta própria
        self.__veterinarios: list[Veterinario] = []
        self.__tutores: list[Tutor] = []
        self.__servicos: list[Servico] = []
        self.__atendimentos: list[Atendimento] = []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome da clínica não pode ser vazio.")
        self.__nome = valor.strip()

    # ---------- cadastros ----------
    def adicionar_veterinario(self, veterinario: Veterinario) -> None:
        if any(v.id == veterinario.id for v in self.__veterinarios):
            raise ValueError(f"Já existe um veterinário com o id {veterinario.id}.")
        self.__veterinarios.append(veterinario)

    def adicionar_tutor(self, tutor: Tutor) -> None:
        if any(t.id == tutor.id for t in self.__tutores):
            raise ValueError(f"Já existe um tutor com o id {tutor.id}.")
        self.__tutores.append(tutor)

    def remover_tutor(self, tutor: Tutor) -> None:
        # os pets são do tutor (composição), então saem junto com ele;
        # os atendimentos já registrados continuam no histórico da clínica
        if tutor not in self.__tutores:
            raise ValueError("Este tutor não está cadastrado na clínica.")
        self.__tutores.remove(tutor)

    def adicionar_servico(self, servico: Servico) -> None:
        if any(s.id == servico.id for s in self.__servicos):
            raise ValueError(f"Já existe um serviço com o id {servico.id}.")
        self.__servicos.append(servico)

    def remover_servico(self, servico: Servico) -> None:
        if servico not in self.__servicos:
            raise ValueError("Este serviço não está no catálogo da clínica.")
        em_uso = any(a.servico is servico and a.status == StatusAtendimento.AGENDADO
                     for a in self.__atendimentos)
        if em_uso:
            raise ValueError("Não é possível excluir um serviço com atendimentos agendados.")
        self.__servicos.remove(servico)

    def listar_veterinarios(self) -> list[Veterinario]:
        return list(self.__veterinarios)

    def listar_tutores(self) -> list[Tutor]:
        return list(self.__tutores)

    def listar_servicos(self) -> list[Servico]:
        return list(self.__servicos)

    def listar_atendimentos(self) -> list[Atendimento]:
        return list(self.__atendimentos)

    # ---------- regras de negócio ----------
    def horario_disponivel(self, vet: Veterinario, pet: Pet, data_hora: datetime,
                           duracao_min: int = 30, ignorar: Atendimento = None) -> bool:
        """RN01: o veterinário e o pet precisam estar livres no horário."""
        fim = data_hora + timedelta(minutes=duracao_min)
        for a in self.__atendimentos:
            if a is ignorar or a.status == StatusAtendimento.CANCELADO:
                continue
            if a.veterinario is not vet and a.pet is not pet:
                continue
            # dois intervalos se sobrepõem quando cada um começa antes do outro terminar
            if a.data_hora < fim and data_hora < a.fim:
                return False
        return True

    def agendar(self, atendimento: Atendimento, solicitante: Usuario = None) -> bool:
        self.__verificar_solicitante(atendimento.pet, solicitante, "agendar_atendimento")
        if atendimento.veterinario not in self.__veterinarios:
            raise ValueError("O veterinário não está cadastrado nesta clínica.")
        if atendimento.servico not in self.__servicos:
            raise ValueError("O serviço não faz parte do catálogo da clínica.")
        if atendimento in self.__atendimentos:
            raise ValueError("Este atendimento já foi agendado.")
        if not self.horario_disponivel(atendimento.veterinario, atendimento.pet,
                                       atendimento.data_hora, atendimento.duracao_min):
            return False
        atendimento.status = StatusAtendimento.AGENDADO
        self.__atendimentos.append(atendimento)
        return True

    def cancelar(self, atendimento: Atendimento, solicitante: Usuario = None,
                 agora: datetime = None) -> bool:
        self.__verificar_solicitante(atendimento.pet, solicitante, "cancelar_atendimento")
        agora = agora or datetime.now()
        if atendimento not in self.__atendimentos or atendimento.status != StatusAtendimento.AGENDADO:
            return False
        # RN04: só pode cancelar com pelo menos 24 horas de antecedência
        if atendimento.data_hora - agora < ANTECEDENCIA_MINIMA:
            return False
        atendimento.status = StatusAtendimento.CANCELADO
        return True

    def remarcar(self, atendimento: Atendimento, nova_data_hora: datetime,
                 solicitante: Usuario = None, agora: datetime = None) -> bool:
        self.__verificar_solicitante(atendimento.pet, solicitante, "remarcar_atendimento")
        agora = agora or datetime.now()
        if atendimento not in self.__atendimentos or atendimento.status != StatusAtendimento.AGENDADO:
            return False
        # RN04: só pode remarcar com pelo menos 24 horas de antecedência
        if atendimento.data_hora - agora < ANTECEDENCIA_MINIMA:
            return False
        if nova_data_hora <= agora:
            return False
        # RN01 também vale para o novo horário (ignorando o próprio atendimento)
        if not self.horario_disponivel(atendimento.veterinario, atendimento.pet,
                                       nova_data_hora, atendimento.duracao_min,
                                       ignorar=atendimento):
            return False
        atendimento.data_hora = nova_data_hora
        return True

    def consultar_historico(self, pet: Pet, solicitante: Usuario) -> list[Atendimento]:
        """UC08 com a RN02: o tutor só vê o histórico dos próprios pets."""
        self.__verificar_solicitante(pet, solicitante, "consultar_historico_clinico")
        historico = [a for a in self.__atendimentos if a.pet is pet]
        return sorted(historico, key=lambda a: a.data_hora)

    def __verificar_solicitante(self, pet: Pet, solicitante: Usuario, permissao: str) -> None:
        if solicitante is None:
            return
        if permissao not in solicitante.obter_permissoes():
            raise PermissionError(f"{solicitante.nome} não tem permissão para esta ação.")
        # RN02: o tutor só acessa os pets ligados ao seu cadastro
        if isinstance(solicitante, Tutor) and pet not in solicitante.listar_pets():
            raise PermissionError("O tutor só pode acessar os próprios pets (RN02).")
