from abc import ABC, abstractmethod


class Usuario(ABC):
    """Classe base abstrata de todas as pessoas que usam o sistema."""

    def __init__(self, id: int, nome: str, cpf: str, telefone: str, senha: str):
        # o id não muda depois de criado, por isso não tem setter
        if not isinstance(id, int) or id <= 0:
            raise ValueError("O id deve ser um número inteiro positivo.")
        self._id = id

        # nome, cpf e telefone passam pelos setters, que fazem a validação
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

        # a senha é privada e só é conferida pelo autenticar()
        if not isinstance(senha, str) or len(senha) < 4:
            raise ValueError("A senha deve ter pelo menos 4 caracteres.")
        self.__senha = senha

    @property
    def id(self) -> int:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome não pode ser vazio.")
        self._nome = valor.strip()

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("O CPF deve ser um texto.")
        # aceita com ou sem pontuação e guarda só os números
        limpo = valor.replace(".", "").replace("-", "").strip()
        if not (limpo.isdigit() and len(limpo) == 11):
            raise ValueError("O CPF deve ter 11 dígitos numéricos.")
        self._cpf = limpo

    @property
    def telefone(self) -> str:
        return self._telefone

    @telefone.setter
    def telefone(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("O telefone deve ser um texto.")
        limpo = valor.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not (limpo.isdigit() and len(limpo) in (10, 11)):
            raise ValueError("O telefone deve ter 10 ou 11 dígitos numéricos.")
        self._telefone = limpo

    def autenticar(self, senha: str) -> bool:
        return self.__senha == senha

    @abstractmethod
    def obter_permissoes(self) -> list[str]:
        """Cada tipo de usuário define o que pode fazer no sistema."""
        pass

    def __str__(self) -> str:
        return f"[{self._id}] {self._nome}"
