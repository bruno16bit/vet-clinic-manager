# Vet Clinic Manager — Sistema de Gestão de Clínica Veterinária

Sistema orientado a objetos em Python para a gestão operacional de clínicas veterinárias. Reúne controle de acesso por perfil de usuário, cadastro de tutores e pets, catálogo de serviços, agendamento sem conflito de horários, prontuário eletrônico e cálculo de custos dos atendimentos.

Projeto acadêmico desenvolvido na disciplina de **Programação Orientada a Objetos (POO)** do **Instituto Federal Catarinense (IFC) — Campus Concórdia**.

## Equipe

- **Bruno M. Ferrari** (`@bruno16bit`)
- **Lucas M. Rosa** (`@mayanrosa`)

## Sumário

1. [Tecnologias](#tecnologias)
2. [Como executar](#como-executar)
3. [Pilares da POO aplicados](#pilares-da-poo-aplicados)
4. [Diagrama de classes](#diagrama-de-classes)
5. [Regras de negócio](#regras-de-negócio)
6. [Exemplo de polimorfismo](#exemplo-de-polimorfismo)
7. [Estrutura do projeto](#estrutura-do-projeto)
8. [Exemplo de execução](#exemplo-de-execução)
9. [Limitações e melhorias futuras](#limitações-e-melhorias-futuras)
10. [Licença](#licença)

---

## Tecnologias

- **Python 3.10+** (desenvolvido e testado no Python 3.14)
- Apenas a biblioteca padrão do Python, sem dependências externas:
  - `abc` — classes e métodos abstratos
  - `enum` — status dos atendimentos
  - `datetime` — datas, horários e antecedência mínima
  - `unittest` — suíte de testes automatizados

---

## Como executar

### 1. Clonar o repositório
```bash
git clone [https://github.com/bruno16bit/vet-clinic-manager.git](https://github.com/bruno16bit/vet-clinic-manager.git)
cd vet-clinic-manager