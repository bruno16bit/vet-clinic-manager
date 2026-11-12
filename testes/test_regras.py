import os
import sys
import unittest
from datetime import datetime

# permite rodar este arquivo direto, a partir de qualquer pasta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from animais.pet import Pet
from atendimentos.atendimento import Atendimento
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

AGORA = datetime(2030, 1, 1, 8, 0)    # "hoje" fixo, para os testes não dependerem do relógio
DIA = datetime(2030, 1, 10, 9, 0)     # atendimento daqui a vários dias


class BaseTeste(unittest.TestCase):
    def setUp(self):
        self.clinica = Clinica("Clínica Teste")
        self.vet = Veterinario(1, "Ana", "11122233344", "49988887777", "vet1", "CRMV-SC 1", "Clínico geral")
        self.vet2 = Veterinario(2, "Beto", "22233344455", "49977776666", "vet2", "CRMV-SC 2", "Cirurgia")
        self.tutor = Tutor(3, "Carlos", "33344455566", "49966665555", "tut1", "carlos@mail.com")
        self.outro_tutor = Tutor(4, "Dora", "44455566677", "49955554444", "tut2", "dora@mail.com")
        self.pet = Pet(1, "Rex", "Cachorro", "SRD", 3)
        self.outro_pet = Pet(2, "Mia", "Gato", "Siamês", 2)
        self.pet_da_dora = Pet(3, "Bolinha", "Cachorro", "Poodle", 5)
        self.tutor.adicionar_pet(self.pet)
        self.tutor.adicionar_pet(self.outro_pet)
        self.outro_tutor.adicionar_pet(self.pet_da_dora)
        self.consulta = Servico(1, "Consulta", 100.0)
        self.cirurgia = Servico(2, "Castração", 200.0)
        self.recepcionista = Recepcionista(5, "Eva", "55566677788", "49944443333", "rec1", "manhã")
        self.admin = Administrador(6, "Paulo", "66677788899", "49933332222", "adm1", "integral", 3)

        for v in (self.vet, self.vet2):
            self.clinica.adicionar_veterinario(v)
        for t in (self.tutor, self.outro_tutor):
            self.clinica.adicionar_tutor(t)
        for s in (self.consulta, self.cirurgia):
            self.clinica.adicionar_servico(s)

    def nova_consulta(self, id, pet=None, vet=None, hora=DIA, exames=0.0):
        return ConsultaMedica(id, pet or self.pet, vet or self.vet, self.consulta, hora,
                              valor_exames=exames)


class TestRN01ConflitoDeAgenda(BaseTeste):
    def test_agenda_em_horario_livre(self):
        self.assertTrue(self.clinica.agendar(self.nova_consulta(1)))

    def test_conflito_do_mesmo_veterinario(self):
        self.clinica.agendar(self.nova_consulta(1))
        outra = self.nova_consulta(2, pet=self.pet_da_dora, hora=datetime(2030, 1, 10, 9, 15))
        self.assertFalse(self.clinica.agendar(outra))

    def test_conflito_do_mesmo_pet(self):
        self.clinica.agendar(self.nova_consulta(1))
        outra = self.nova_consulta(2, vet=self.vet2, hora=datetime(2030, 1, 10, 9, 20))
        self.assertFalse(self.clinica.agendar(outra))

    def test_horario_logo_depois_esta_livre(self):
        self.clinica.agendar(self.nova_consulta(1))
        seguinte = self.nova_consulta(2, hora=datetime(2030, 1, 10, 9, 30))  # 30 min depois
        self.assertTrue(self.clinica.agendar(seguinte))

    def test_cancelado_libera_o_horario(self):
        primeira = self.nova_consulta(1)
        self.clinica.agendar(primeira)
        self.clinica.cancelar(primeira, agora=AGORA)
        self.assertTrue(self.clinica.agendar(self.nova_consulta(2)))


class TestRN02AcessoDoTutor(BaseTeste):
    def test_tutor_ve_historico_do_proprio_pet(self):
        self.clinica.agendar(self.nova_consulta(1))
        historico = self.clinica.consultar_historico(self.pet, self.tutor)
        self.assertEqual(len(historico), 1)

    def test_tutor_nao_ve_historico_de_pet_alheio(self):
        with self.assertRaises(PermissionError):
            self.clinica.consultar_historico(self.pet_da_dora, self.tutor)

    def test_tutor_nao_agenda_para_pet_alheio(self):
        alheia = self.nova_consulta(1, pet=self.pet_da_dora)
        with self.assertRaises(PermissionError):
            self.clinica.agendar(alheia, solicitante=self.tutor)

    def test_tutor_agenda_para_o_proprio_pet(self):
        self.assertTrue(self.clinica.agendar(self.nova_consulta(1), solicitante=self.tutor))

    def test_veterinario_nao_agenda(self):
        with self.assertRaises(PermissionError):
            self.clinica.agendar(self.nova_consulta(1), solicitante=self.vet)

    def test_veterinario_consulta_historico_de_qualquer_pet(self):
        self.clinica.agendar(self.nova_consulta(1, pet=self.pet_da_dora))
        self.assertEqual(len(self.clinica.consultar_historico(self.pet_da_dora, self.vet)), 1)


class TestRN03CustoDoAtendimento(BaseTeste):
    def test_custo_da_consulta_soma_exames(self):
        consulta = self.nova_consulta(1, exames=50.0)
        self.assertEqual(consulta.calcular_custo(), 150.0)

    def test_custo_da_cirurgia_soma_anestesia_e_taxa(self):
        cirurgia = ProcedimentoCirurgico(2, self.pet, self.vet2, self.cirurgia, DIA,
                                         taxa_anestesia=80.0, taxa_cirurgica=120.0)
        self.assertEqual(cirurgia.calcular_custo(), 400.0)

    def test_polimorfismo_do_calcular_custo(self):
        atendimentos = [
            self.nova_consulta(1, exames=50.0),
            ProcedimentoCirurgico(2, self.pet, self.vet2, self.cirurgia, DIA,
                                  taxa_anestesia=80.0, taxa_cirurgica=120.0),
        ]
        # a mesma chamada, comportamentos diferentes
        self.assertEqual([a.calcular_custo() for a in atendimentos], [150.0, 400.0])

    def test_atendimento_e_abstrato(self):
        with self.assertRaises(TypeError):
            Atendimento(1, self.pet, self.vet, self.consulta, DIA)


class TestRN04Antecedencia(BaseTeste):
    def test_cancela_com_mais_de_24h(self):
        atendimento = self.nova_consulta(1)
        self.clinica.agendar(atendimento)
        self.assertTrue(self.clinica.cancelar(atendimento, agora=AGORA))
        self.assertEqual(atendimento.status, StatusAtendimento.CANCELADO)

    def test_nao_cancela_com_menos_de_24h(self):
        atendimento = self.nova_consulta(1)
        self.clinica.agendar(atendimento)
        vespera = datetime(2030, 1, 9, 10, 0)    # 23h antes do atendimento
        self.assertFalse(self.clinica.cancelar(atendimento, agora=vespera))
        self.assertEqual(atendimento.status, StatusAtendimento.AGENDADO)

    def test_remarca_com_mais_de_24h(self):
        atendimento = self.nova_consulta(1)
        self.clinica.agendar(atendimento)
        novo = datetime(2030, 1, 12, 15, 0)
        self.assertTrue(self.clinica.remarcar(atendimento, novo, agora=AGORA))
        self.assertEqual(atendimento.data_hora, novo)

    def test_nao_remarca_com_menos_de_24h(self):
        atendimento = self.nova_consulta(1)
        self.clinica.agendar(atendimento)
        vespera = datetime(2030, 1, 9, 10, 0)
        self.assertFalse(self.clinica.remarcar(atendimento, datetime(2030, 1, 12, 9, 0), agora=vespera))
        self.assertEqual(atendimento.data_hora, DIA)

    def test_nao_remarca_para_horario_ocupado(self):
        self.clinica.agendar(self.nova_consulta(1))
        outro = self.nova_consulta(2, pet=self.outro_pet, hora=datetime(2030, 1, 11, 9, 0))
        self.clinica.agendar(outro)
        self.assertFalse(self.clinica.remarcar(outro, DIA, agora=AGORA))   # cairia em cima da consulta 1


class TestOutrasRegras(BaseTeste):
    def test_usuario_e_abstrato(self):
        with self.assertRaises(TypeError):
            Usuario(1, "A", "12345678901", "49999990000", "abcd")

    def test_validacoes_dos_setters(self):
        with self.assertRaises(ValueError):
            Tutor(9, "X", "123", "49999990000", "abcd", "x@mail.com")      # CPF inválido
        with self.assertRaises(ValueError):
            Servico(9, "Banho", -10)                                       # preço negativo

    def test_prontuario_pertence_ao_atendimento(self):
        atendimento = self.nova_consulta(1)
        prontuario = self.vet.registrar_prontuario(atendimento, "Gripe leve", "Repouso")
        self.assertIs(atendimento.prontuario, prontuario)
        with self.assertRaises(ValueError):
            self.vet.registrar_prontuario(atendimento, "Outro registro")   # já tem prontuário

    def test_permissoes_do_administrador_incluem_as_da_recepcionista(self):
        permissoes_adm = self.admin.obter_permissoes()
        for permissao in self.recepcionista.obter_permissoes():
            self.assertIn(permissao, permissoes_adm)
        self.assertIn("emitir_relatorio", permissoes_adm)
        self.assertNotIn("emitir_relatorio", self.recepcionista.obter_permissoes())

    def test_relatorio_soma_so_os_concluidos(self):
        concluido = self.nova_consulta(1, exames=50.0)
        agendado = self.nova_consulta(2, pet=self.outro_pet, hora=datetime(2030, 1, 11, 9, 0))
        self.clinica.agendar(concluido)
        self.clinica.agendar(agendado)
        concluido.status = StatusAtendimento.CONCLUIDO
        relatorio = self.admin.emitir_relatorio(self.clinica)
        self.assertIn("R$ 150.00", relatorio)
        self.assertIn("Total de atendimentos: 2", relatorio)

    def test_recepcionista_cadastra_e_exclui_tutor(self):
        novo = Tutor(7, "Fabio", "77788899900", "49922221111", "tut3", "fabio@mail.com")
        self.recepcionista.cadastrar_tutor(novo, self.clinica)
        self.assertIn(novo, self.clinica.listar_tutores())
        self.recepcionista.excluir_tutor(novo, self.clinica)
        self.assertNotIn(novo, self.clinica.listar_tutores())


if __name__ == "__main__":
    unittest.main(verbosity=2)