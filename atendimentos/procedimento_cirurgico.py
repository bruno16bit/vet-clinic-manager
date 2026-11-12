from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING

from atendimentos.atendimento import Atendimento

if TYPE_CHECKING:
    from animais.pet import Pet
    from usuarios.veterinario import Veterinario
    from clinica.servico import Servico


class ProcedimentoCirurgico(Atendimento):
    def __init__(self, id: int, pet: Pet, veterinario: Veterinario, servico: Servico,
                 data_hora: datetime, duracao_min: int = 30,
                 taxa_anestesia: float = 0.0, taxa_cirurgica: float = 0.0):
        super().__init__(id, pet, veterinario, servico, data_hora, duracao_min)
        self.taxa_anestesia = taxa_anestesia
        self.taxa_cirurgica = taxa_cirurgica

    @property
    def taxa_anestesia(self) -> float:
        return self.__taxa_anestesia

    @taxa_anestesia.setter
    def taxa_anestesia(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("A taxa de anestesia não pode ser negativa.")
        self.__taxa_anestesia = float(valor)

    @property
    def taxa_cirurgica(self) -> float:
        return self.__taxa_cirurgica

    @taxa_cirurgica.setter
    def taxa_cirurgica(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("A taxa cirúrgica não pode ser negativa.")
        self.__taxa_cirurgica = float(valor)

    def calcular_custo(self) -> float:
        # RN03: no procedimento cirúrgico, o valor do serviço soma anestesia e taxa cirúrgica
        return self.servico.preco + self.__taxa_anestesia + self.__taxa_cirurgica