from datetime import datetime, timedelta

from animais.pet import Pet
from atendimentos.consulta_medica import ConsultaMedica
from atendimentos.procedimento_cirurgico import ProcedimentoCirurgico
from atendimentos.status_atendimento import StatusAtendimento
from clinica.clinica import Clinica
from clinica.servico import Servico
from usuarios.administrador import Administrador
from usuarios.recepcionista import Recepcionista
from usuarios.tutor import Tutor
from usuarios.usuario import Usuario
from usuarios.veterinario import Veterinario


def titulo(texto: str) -> None:
    print(f"\n=== {texto} ===")


def main() -> None:
    clinica = Clinica("Clínica Veterinária Patinhas")

    # ---------- cadastros ----------
    titulo("Cadastros")
    ana = Veterinario(1, "Ana Souza", "111.222.333-44", "(49) 98888-7777", "vet1", "crmv-sc 1234", "Clínica geral")
    beto = Veterinario(2, "Beto Lima", "222.333.444-55", "(49) 97777-6666", "vet2", "crmv-sc 5678", "Cirurgia")
    eva = Recepcionista(3, "Eva Martins", "555.666.777-88", "(49) 94444-3333", "rec1", "manhã")
    paulo = Administrador(4, "Paulo Ramos", "666.777.888-99", "(49) 93333-2222", "adm1", "integral", 3)
    clinica.adicionar_veterinario(ana)
    clinica.adicionar_veterinario(beto)

    consulta = Servico(1, "Consulta", 100.0)
    castracao = Servico(2, "Castração", 200.0)
    paulo.cadastrar_servico(consulta, clinica)
    paulo.cadastrar_servico(castracao, clinica)

    carlos = Tutor(5, "Carlos Pereira", "333.444.555-66", "(49) 96666-5555", "tut1", "carlos@mail.com")
    dora = Tutor(6, "Dora Alves", "444.555.666-77", "(49) 95555-4444", "tut2", "dora@mail.com")
    rex = Pet(1, "Rex", "Cachorro", "SRD", 3)
    mia = Pet(2, "Mia", "Gato", "Siamês", 2)
    bolinha = Pet(3, "Bolinha", "Cachorro", "Poodle", 5)
    for tutor, pets in ((carlos, [rex, mia]), (dora, [bolinha])):
        eva.cadastrar_tutor(tutor, clinica)
        for pet in pets:
            eva.cadastrar_pet(tutor, pet)
    print(f"Tutores: {[t.nome for t in clinica.listar_tutores()]}")
    print(f"Pets do Carlos: {[p.obter_dados() for p in carlos.listar_pets()]}")
    print(f"Serviços: {[str(s) for s in clinica.listar_servicos()]}")

    # ---------- agendamento e RN01 ----------
    titulo("Agendamento (RN01: conflito de agenda)")
    dia = (datetime.now() + timedelta(days=3)).replace(hour=9, minute=0, second=0, microsecond=0)

    consulta_rex = ConsultaMedica(1, rex, ana, consulta, dia, valor_exames=50.0)
    print("Tutor agenda consulta do Rex às 09:00:", clinica.agendar(consulta_rex, solicitante=carlos))

    conflito = ConsultaMedica(2, bolinha, ana, consulta, dia + timedelta(minutes=15))
    print("Outra consulta com a Ana às 09:15 (conflito):", clinica.agendar(conflito, solicitante=dora))

    cirurgia_mia = ProcedimentoCirurgico(3, mia, beto, castracao, dia + timedelta(hours=1),
                                         taxa_anestesia=80.0, taxa_cirurgica=120.0)
    print("Recepcionista agenda a cirurgia da Mia às 10:00:",
          eva.agendar_atendimento(cirurgia_mia, clinica))

    # ---------- RN02 ----------
    titulo("Acesso do tutor (RN02)")
    historico = clinica.consultar_historico(rex, carlos)
    print(f"Carlos vê o histórico do Rex: {len(historico)} atendimento(s)")
    try:
        clinica.consultar_historico(bolinha, carlos)
    except PermissionError as erro:
        print("Carlos tenta ver o histórico da Bolinha ->", erro)

    # ---------- RN03 e polimorfismo ----------
    titulo("Custo do atendimento (RN03) e polimorfismo")
    for atendimento in clinica.listar_atendimentos():
        print(atendimento.obter_resumo())

    # ---------- prontuário ----------
    titulo("Prontuário")
    prontuario = ana.registrar_prontuario(consulta_rex, "Rex com tosse leve, sem febre.", "Xarope por 5 dias.")
    print(prontuario.obter_texto())
    consulta_rex.status = StatusAtendimento.CONCLUIDO

    # ---------- RN04 ----------
    titulo("Remarcar e cancelar (RN04: 24h de antecedência)")
    nova_data = dia + timedelta(days=1, hours=5)
    print("Remarcar a cirurgia da Mia para o dia seguinte às 14:00:",
          clinica.remarcar(cirurgia_mia, nova_data, solicitante=carlos))

    urgente = ConsultaMedica(4, mia, ana, consulta, datetime.now() + timedelta(hours=5))
    clinica.agendar(urgente)
    print("Cancelar consulta que é daqui a 5 horas (menos de 24h):", clinica.cancelar(urgente))

    cancelavel = ConsultaMedica(5, bolinha, ana, consulta, dia + timedelta(days=2))
    clinica.agendar(cancelavel)
    print("Cancelar consulta que é daqui a 2 dias:", clinica.cancelar(cancelavel, solicitante=dora))

    # ---------- relatório ----------
    titulo("Relatório do administrador")
    print(paulo.emitir_relatorio(clinica))

    # ---------- permissões (polimorfismo em obter_permissoes) ----------
    titulo("Permissões de cada tipo de usuário")
    for usuario in (carlos, ana, eva, paulo):
        print(f"{type(usuario).__name__:<13} {usuario.nome}: {usuario.obter_permissoes()}")

    # ---------- classe abstrata e exclusão ----------
    titulo("Classe abstrata e exclusão de cadastro")
    try:
        Usuario(9, "Fulano", "12345678901", "49999990000", "abcd")
    except TypeError as erro:
        print("Instanciar Usuario direto ->", erro)

    eva.excluir_tutor(dora, clinica)
    print(f"Tutores depois de excluir a Dora: {[t.nome for t in clinica.listar_tutores()]}")


if __name__ == "__main__":
    main()