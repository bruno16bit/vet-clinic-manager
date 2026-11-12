class Pet:
    def __init__(self, id: int, nome: str, especie: str, raca: str, idade: int):
        # o id não muda depois de criado, por isso não tem setter
        if not isinstance(id, int) or id <= 0:
            raise ValueError("O id do pet deve ser um número inteiro positivo.")
        self.__id = id
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.idade = idade

    @property
    def id(self) -> int:
        return self.__id

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome do pet não pode ser vazio.")
        self.__nome = valor.strip()

    @property
    def especie(self) -> str:
        return self.__especie

    @especie.setter
    def especie(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("A espécie do pet não pode ser vazia.")
        self.__especie = valor.strip()

    @property
    def raca(self) -> str:
        return self.__raca

    @raca.setter
    def raca(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("A raça do pet não pode ser vazia (use SRD se não tiver raça definida).")
        self.__raca = valor.strip()

    @property
    def idade(self) -> int:
        return self.__idade

    @idade.setter
    def idade(self, valor: int) -> None:
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("A idade do pet deve ser um número inteiro maior ou igual a zero.")
        self.__idade = valor

    def obter_dados(self) -> str:
        return f"{self.__nome} ({self.__especie}, {self.__raca}), {self.__idade} ano(s)"

    def __str__(self) -> str:
        return f"[{self.__id}] {self.__nome}"