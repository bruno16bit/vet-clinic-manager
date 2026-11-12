class Servico:
    def __init__(self, id: int, nome: str, preco: float):
        # o id não muda depois de criado, por isso não tem setter
        if not isinstance(id, int) or id <= 0:
            raise ValueError("O id do serviço deve ser um número inteiro positivo.")
        self.__id = id
        self.nome = nome
        self.preco = preco

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome do serviço não pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, valor: float) -> None:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("O preço do serviço não pode ser negativo.")
        self.__preco = float(valor)

    def obter_preco(self) -> float:
        return self.__preco

    def __str__(self) -> str:
        return f"{self.__nome} (R$ {self.__preco:.2f})"