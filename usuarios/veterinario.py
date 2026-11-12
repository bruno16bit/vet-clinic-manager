from usuarios.usuario import Usuario


class Veterinario(Usuario):
    def __init__(self, id: int, nome: str, cpf: str, telefone: str, senha: str, crmv: str, especialidade: str):
        super().__init__(id, nome, cpf, telefone, senha)
        self.crmv = crmv
        self.especialidade = especialidade

    @property
    def crmv(self) -> str:
        return self._crmv

    @crmv.setter
    def crmv(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O CRMV não pode ser vazio.")
        self._crmv = valor.strip().upper()

    @property
    def especialidade(self) -> str:
        return self._especialidade

    @especialidade.setter
    def especialidade(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("A especialidade não pode ser vazia.")
        self._especialidade = valor.strip()

    def registrar_prontuario(self, atendimento, texto: str, prescricao: str = ""):
        # Implementação integrada com Prontuario / Atendimento
        pass

    def obter_permissoes(self) -> list[str]:
        return ["registrar_prontuario", "visualizar_atendimentos", "visualizar_pets"]