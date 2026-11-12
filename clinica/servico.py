class Servico:
    def __init__(self, id: int, nome: str, preco: float):
        self.__id = id
        self.nome = nome
        self.preco = preco

    def obter_preco(self, preco: float):
        self.preco = preco

    @property
    def preco(self):
        return self.preco
    @preco.setter
    def preco(self, preco: float):
        self.preco = preco

    @property
    def nome(self):
        return self.nome
    @nome.setter
    def nome(self, nome: str):
        self.nome = nome

    @property
    def id(self):
        return self.id
    @id.setter
    def id(self, __id: int):
        self.__id = id

    @property
    def obter_preco(self, preco: float):
        self.preco = preco
