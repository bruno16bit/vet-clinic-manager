# Vet Clinic Manager

Sistema de gestão para clínicas veterinárias, feito em **Python** com **programação orientada a objetos**. Cuida de cadastros, agendamento sem conflito de horários, prontuários e do cálculo do valor de cada atendimento, com permissões diferentes para cada perfil de usuário.

Projeto da disciplina de Programação Orientada a Objetos I, no IFC — Campus Concórdia.

## O que o sistema faz

- **Quatro perfis de usuário** (tutor, veterinário, recepcionista e administrador), cada um com suas permissões.
- **Cadastro** de tutores e pets e **catálogo** de serviços com preços.
- **Agendamento, remarcação e cancelamento** de atendimentos, sem choque de horário e com antecedência mínima.
- **Prontuário** registrado pelo veterinário em cada atendimento.
- **Custo calculado por tipo de atendimento** (consulta ou procedimento cirúrgico).
- **Relatório financeiro** para o administrador.
- **Privacidade:** o tutor só enxerga os próprios pets e atendimentos.

## Destaques de POO

- **Abstração:** `Usuario` e `Atendimento` são classes abstratas, com métodos abstratos (`obter_permissoes()` e `calcular_custo()`).
- **Herança:** `Tutor`, `Veterinario` e `Recepcionista` herdam de `Usuario`; `Administrador` herda de `Recepcionista`; `ConsultaMedica` e `ProcedimentoCirurgico` herdam de `Atendimento`.
- **Polimorfismo:** cada subclasse sobrescreve `calcular_custo()` e `obter_permissoes()`, e quem chama não precisa saber o tipo.
- **Encapsulamento:** atributos protegidos (`_x`) e privados (`__x`) com `@property` e validação nos *setters*, então um objeto nunca fica em estado inválido.
- **Relações:** composição (`Tutor`–`Pet`, `Atendimento`–`Prontuario`), agregação (`Clinica`) e associação.

## Como executar

Só precisa do **Python 3.10 ou superior**, sem instalar bibliotecas. Rode os comandos na pasta raiz do projeto:

```bash
git clone https://github.com/bruno16bit/vet-clinic-manager.git
cd vet-clinic-manager

python main.py                           # demonstração do sistema
python -m unittest testes.test_regras -v # testes das regras de negócio
```

## Exemplo de uso

```python
from datetime import datetime
from animais.pet import Pet
from atendimentos.consulta_medica import ConsultaMedica
from clinica.clinica import Clinica
from clinica.servico import Servico
from usuarios.tutor import Tutor
from usuarios.veterinario import Veterinario

clinica = Clinica("Clínica Patinhas")
ana = Veterinario(1, "Ana Souza", "111.222.333-44", "(49) 98888-7777", "senha1", "CRMV-SC 1234", "Clínica geral")
consulta = Servico(1, "Consulta", 100.0)
carlos = Tutor(2, "Carlos", "333.444.555-66", "(49) 96666-5555", "senha2", "carlos@mail.com")
rex = Pet(1, "Rex", "Cachorro", "SRD", 3)

clinica.adicionar_veterinario(ana)
clinica.adicionar_servico(consulta)
clinica.adicionar_tutor(carlos)
carlos.adicionar_pet(rex)

atendimento = ConsultaMedica(1, rex, ana, consulta, datetime(2026, 11, 20, 9, 0), valor_exames=50.0)
clinica.agendar(atendimento, solicitante=carlos)   # True
print(atendimento.obter_resumo())
```

```text
[1] ConsultaMedica | Pet: Rex | Vet: Ana Souza | 20/11/2026 09:00 | Agendado | R$ 150.00
```

## Regras de negócio

| Regra | Descrição |
|---|---|
| **RN01** | O agendamento só é confirmado se o veterinário e o pet estiverem livres no horário (cada atendimento ocupa 30 minutos). |
| **RN02** | O tutor só acessa os pets e atendimentos ligados ao seu cadastro. Acesso indevido gera `PermissionError`. |
| **RN03** | Consulta: serviço + exames. Procedimento cirúrgico: serviço + anestesia + taxa cirúrgica. |
| **RN04** | Remarcar ou cancelar exige no mínimo 24 horas de antecedência. |

Quando RN01 ou RN04 impedem a operação, o método devolve `False`. Dados inválidos geram `ValueError`. Os **26 testes** automatizados cobrem as quatro regras, as classes abstratas, as validações, os prontuários, as permissões e o relatório.

## Estrutura do projeto

```text
vet-clinic-manager/
├── animais/          # Pet
├── atendimentos/     # Atendimento (abstrata), ConsultaMedica, ProcedimentoCirurgico,
│                     # Prontuario e StatusAtendimento
├── clinica/          # Clinica (regras de negócio) e Servico
├── usuarios/         # Usuario (abstrata), Tutor, Veterinario, Recepcionista, Administrador
├── testes/           # test_regras.py
└── main.py           # demonstração
```

## Decisões de projeto

- **Código fiel à modelagem:** as classes e relações seguem o diagrama UML. Os ajustes foram pequenos: as associações do UML viraram atributos (por exemplo, `Atendimento` guarda `pet`, `veterinario` e `servico`) e alguns métodos receberam a `Clinica` como parâmetro.
- **Resultado em vez de exceção nas regras de agenda:** `agendar`, `cancelar` e `remarcar` devolvem `True` ou `False`. Exceções ficam para uso inválido e falta de permissão.
- **Tempo injetável:** `cancelar` e `remarcar` aceitam o parâmetro `agora`, o que permite testar a regra das 24 horas sem depender do relógio.

## Limitações e próximos passos

- Os dados ficam em memória, então somem quando o programa fecha. Persistência em arquivo ou banco de dados é o próximo passo natural.
- A senha é guardada em texto puro (simplificação do trabalho). Em um sistema real seria usado *hash*.
- O CPF é validado só pelo formato, sem conferir os dígitos verificadores.
- Interface gráfica com **Tkinter**, que vem na próxima etapa do projeto.

## Autores

- **Bruno M. Ferrari** — [@bruno16bit](https://github.com/bruno16bit)
- **Lucas M. Rosa** — [@mayanrosa](https://github.com/mayanrosa)

Projeto acadêmico desenvolvido para fins educacionais.