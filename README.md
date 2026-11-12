# Vet Clinic Manager — Veterinary Clinic Management System

An Object-Oriented **Python** system designed for the operational management of veterinary clinics, featuring role-based user access control, owner and pet registration, service catalog management, conflict-free appointment scheduling, electronic medical records, and financial reporting.

Developed as an academic project for the **Object-Oriented Programming (OOP)** course at **Instituto Federal Catarinense (IFC) — Campus Concórdia**.

---

## Team Members

* **Bruno M. Ferrari** (`@bruno16bit`)
* **Lucas M. Rosa**

---

## Applied OOP Pillars

The project was architected by strictly applying the four pillars of Object-Oriented Programming:

* **Abstraction:** Abstract base classes (`ABC` and `@abstractmethod`) in `Usuario` and `Atendimento`, defining mandatory contracts (`obter_permissoes()` and `calcular_custo()`) while preventing direct instantiation.
* **Encapsulation:** Protected (`_`) and private (`__`) attributes with defensive validation via `@property` and setters (preventing invalid IDs, negative prices, malformed emails, and non-standard CPF/phone numbers).
* **Inheritance:**
  * User hierarchy: `Usuario` $\rightarrow$ `Tutor`, `Veterinario`, `Recepcionista` $\rightarrow$ `Administrador`.
  * Appointment hierarchy: `Atendimento` $\rightarrow$ `ConsultaMedica` and `ProcedimentoCirurgico`.
* **Polymorphism:** Method overriding in `calcular_custo()` (adding exam fees to medical consultations and anesthesia/surgical fees to surgical procedures) and in `obter_permissoes()` according to each user's role.
* **Relationships (Composition, Aggregation, and Association):**
  * *Composition:* `Atendimento` $\rightarrow$ `Prontuario` and `Tutor` $\rightarrow$ `Pet`.
  * *Aggregation:* `Clinica` managing collections of `Veterinario`, `Tutor`, `Servico`, and `Atendimento`.

---

## Implemented Business Rules

* **RN01 — Schedule Conflict Prevention:** Prevents booking or rescheduling overlapping time slots for the same veterinarian or the same pet (ignoring canceled appointments).
* **RN02 — Role-Based Access Control & Owner Privacy:** Each user role has specific permissions; pet owners (`Tutor`) can only schedule, cancel, reschedule, or view the medical history of their own pets.
* **RN03 — Dynamic Cost Calculation:** Medical consultations add the base service price to additional exam costs; surgical procedures add the base service price to anesthesia and surgical fees.
* **RN04 — 24-Hour Minimum Advance Notice:** Cancellations and rescheduling are only allowed at least 24 hours prior to the scheduled appointment time.

---

## Project Structure

```text
vet-clinic-manager/
│
├── animais/
│   ├── __init__.py
│   └── pet.py                      # Pet entity
│
├── atendimentos/
│   ├── __init__.py
│   ├── atendimento.py              # Abstract class Atendimento
│   ├── consulta_medica.py          # Subclass ConsultaMedica
│   ├── procedimento_cirurgico.py   # Subclass ProcedimentoCirurgico
│   ├── prontuario.py               # Prontuario entity (composition)
│   └── status_atendimento.py       # Enum StatusAtendimento (AGENDADO, CONCLUIDO, CANCELADO)
│
├── clinica/
│   ├── __init__.py
│   ├── clinica.py                  # Central controller and business rules (RN01–RN04)
│   └── servico.py                  # Servico entity
│
├── usuarios/
│   ├── __init__.py
│   ├── usuario.py                  # Abstract class Usuario
│   ├── tutor.py                    # Subclass Tutor
│   ├── veterinario.py              # Subclass Veterinario
│   ├── recepcionista.py            # Subclass Recepcionista
│   └── administrador.py            # Subclass Administrador (inherits from Recepcionista)
│
├── testes/
│   └── test_regras.py              # Unit test suite with 26 tests (unittest)
│
├── main.py                         # Full demonstration of system flows and business rules
├── .gitignore
└── README.md
