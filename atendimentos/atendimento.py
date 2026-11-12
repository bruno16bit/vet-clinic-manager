from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from atendimentos.status_atendimento import StatusAtendimento
from atendimentos.prontuario import Prontuario

if TYPE_CHECKING:
    # só para tipagem, não é importado na execução (evita import circular)
    from animais.pet import Pet
    from usuarios.veterinario import Veterinario
    from clinica.servico import Servico


class Atendimento(ABC):
    def __init__(self, id: int, pet: Pet, veterinario: Veterinario, servico: Servico,
                 data_hora: datetime, duracao_min: int = 30):
        # o id não muda depois de criado, por isso não tem setter
        if not isinstance(id, int) or id <= 0:
            raise ValueError("O id do atendimento deve ser um número inteiro positivo.")
        if pet is None or veterinario is None or servico is None:
            raise ValueError("O atendimento precisa de pet, veterinário e serviço.")
        self._id = id
        self._pet = pet
        self._veterinario = veterinario
        self._servico = servico
        self.data_hora = data_hora
        self.duracao_min = duracao_min
        self._status = StatusAtendimento.AGENDADO
        # composição: o prontuário é criado pelo atendimento e não existe sem ele
        self._prontuario = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def pet(self) -> Pet:
        return self._pet

    @property
    def veterinario(self) -> Veterinario:
        return self._veterinario

    @property
    def servico(self) -> Servico:
        return self._servico

    @property
    def data_hora(self) -> datetime:
        return self._data_hora

    @data_hora.setter
    def data_hora(self, valor: datetime) -> None:
        if not isinstance(valor, datetime):
            raise ValueError("A data e hora do atendimento deve ser um datetime.")
        self._data_hora = valor

    @property
    def duracao_min(self) -> int:
        return self._duracao_min

    @duracao_min.setter
    def duracao_min(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("A duração deve ser um número inteiro de minutos maior que zero.")
        self._duracao_min = valor

    @property
    def status(self) -> StatusAtendimento:
        return self._status

    @status.setter
    def status(self, valor: StatusAtendimento) -> None:
        if not isinstance(valor, StatusAtendimento):
            raise ValueError("O status deve ser um valor de StatusAtendimento.")
        self._status = valor

    @property
    def fim(self) -> datetime:
        return self._data_hora + timedelta(minutes=self._duracao_min)

    @property
    def prontuario(self) -> Prontuario | None:
        return self._prontuario

    def criar_prontuario(self, descricao: str, prescricao: str = "") -> Prontuario:
        if self._status == StatusAtendimento.CANCELADO:
            raise ValueError("Não é possível registrar prontuário de um atendimento cancelado.")
        if self._prontuario is not None:
            raise ValueError("Este atendimento já tem prontuário.")
        self._prontuario = Prontuario(descricao, prescricao)
        return self._prontuario

    @abstractmethod
    def calcular_custo(self) -> float:
        """Cada tipo de atendimento calcula o seu valor total."""
        pass

    def obter_resumo(self) -> str:
        return (f"[{self._id}] {type(self).__name__} | Pet: {self._pet.nome} | "
                f"Vet: {self._veterinario.nome} | {self._data_hora:%d/%m/%Y %H:%M} | "
                f"{self._status.value} | R$ {self.calcular_custo():.2f}")