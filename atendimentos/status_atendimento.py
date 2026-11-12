from enum import Enum


class StatusAtendimento(Enum):
    AGENDADO = "Agendado"
    CONCLUIDO = "Concluído"
    CANCELADO = "Cancelado"