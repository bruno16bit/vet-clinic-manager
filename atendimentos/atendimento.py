from abc import ABC, abstractmethod

from datetime import datetime

class Atendimento(ABC):
    def __init__(self, id: int, data_hora: datetime, status: str, duracao_min: int):
        self.__id = id
        self.data_hora = data_hora
        self.status = status
        self.duracao_min = duracao_min

    @property
    def id(self, id: int ):
        return self.__id

    @property
    def data_hora(self, data_hora: datetime):
        return self.data_hora

    @property
    def status(self, status: str):
        return self.status

    @property
    def duracao_min(self, duracao_min: int):
        return self.duracao_min

    @id.setter
    def id(self, id: int):
        self.__id = id

    @data_hora.setter
    def data_hora(self, data_hora: datetime):
        self.data_hora = data_hora

    @status.setter
    def status(self, status: str):
        self.status = status

    @duracao_min.setter
    def duracao_min(self, duracao_min: int):
        self.duracao_min = duracao_min


    @abstractmethod

    def calcular_custo():
        pass

    def obter_resumo():
        pass