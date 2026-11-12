from datetime import datetime


class Prontuario:
    # contador da classe, usado para gerar o id de cada prontuário
    __contador = 0

    def __init__(self, descricao: str, prescricao: str = "", data_registro: datetime = None):
        self.descricao = descricao
        self.prescricao = prescricao
        if data_registro is not None and not isinstance(data_registro, datetime):
            raise ValueError("A data do registro deve ser um datetime.")
        self.__data_registro = data_registro or datetime.now()
        Prontuario.__contador += 1
        self.__id = Prontuario.__contador

    @property
    def id(self) -> int:
        return self.__id

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("A descrição do prontuário não pode ser vazia.")
        self.__descricao = valor.strip()

    @property
    def prescricao(self) -> str:
        return self.__prescricao

    @prescricao.setter
    def prescricao(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("A prescrição deve ser um texto.")
        self.__prescricao = valor.strip()

    @property
    def data_registro(self) -> datetime:
        return self.__data_registro

    def obter_texto(self) -> str:
        texto = f"Prontuário {self.__id} ({self.__data_registro:%d/%m/%Y %H:%M})\n"
        texto += f"Descrição: {self.__descricao}"
        if self.__prescricao:
            texto += f"\nPrescrição: {self.__prescricao}"
        return texto