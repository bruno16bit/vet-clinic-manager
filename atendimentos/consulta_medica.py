from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from atendimentos.atendimento import Atendimento

if TYPE_CHECKING:
    from animais.pet import Pet
    from usuarios.veterinario import Veterinario
    from clinica.servico import Servico


class ConsultaMedica(Atendimento):
    def __init__(self, id: int, pet: Pet, veterinario: Veterinario, servico: Servico,
                 data_hora: datetime, duracao_min: int = 30,
                 valor_exames: float = 0.0, diagnostico: str = ""):
        super().__init__(id, pet, veterinario, servico, data_hora, duracao_min)
        self.valor_exames = valor_exames
        self.diagnostico = diagnostico

    @property
    def valor_exames(self) -> float:
        return self.__valor_exames

    @valor_exames.setter
    def valor_exames(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("O valor dos exames não pode ser negativo.")
        self.__valor_exames = float(valor)

    @property
    def diagnostico(self) -> str:
        return self.__diagnostico

    @diagnostico.setter
    def diagnostico(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("O diagnóstico deve ser um texto.")
        self.__diagnostico = valor.strip()

    def calcular_custo(self) -> float:
        # RN03: na consulta, o valor do serviço soma os exames
        return self.servico.preco + self.__valor_exames