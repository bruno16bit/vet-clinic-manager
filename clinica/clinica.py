from datetime import datetime

class Clinica():
    def __init__(self, nome: str):
        self.nome = nome

    def horario_disponivel(self, vet: str, pet: str, data_hora: datetime):
        self.vet = vet
        self.pet = pet
        self.data_hora = data_hora
        #saida tem que ser bool

    def agendar(self, atendimento: str):
        self.atendimento = atendimento
        pass
        #saida tem que ser bool

    def cancelar(atendimento: str):
        pass
        # saida tem que ser bool

    def remarcar(self, atendimento: str, nova_data_hora: datetime):
        pass
        # saida tem que ser bool

    @property
    def nome(self):
        return self.nome
    @nome.setter
    def nome(self, nome: str):
        self.nome = nome

    @property
    def vet(self):
        return self.vet
    @vet.setter
    def vet(self, vet: str):
        self.vet = vet

    @property
    def pet(self):
        return self.pet
    @pet.setter
    def pet(self, pet: str):
        self.pet = pet

    @property
    def data_hora(self):
        return self.data_hora
    @data_hora.setter
    def data_hora(self, data_hora: str):
        self.data_hora = data_hora

    @property
    def atendimento(self):
        return self.atendimento
    @atendimento.setter
    def atendimento(self, atendimento: str):
        self.atendimento = atendimento

