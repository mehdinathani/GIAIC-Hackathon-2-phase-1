# Research: Phase I - CLI Basics

**Branch**: `001-cli-basics` | **Date**: 2025-12-28

## Research Summary

All technical decisions are pre-determined by the Constitution. No NEEDS CLARIFICATION items remain.

---

## Decision 1: CLI Framework

**Decision**: Typer

**Rationale**:
- Mandated by Constitution (Technical Constraints)
- Built on Click with automatic type conversion
- Native support for Python type hints
- Automatic `--help` generation
- Excellent integration with Rich for styled output

**Alternatives Considered**:
- Click: Lower-level, requires more boilerplate
- argparse: Standard library but verbose, no type hint support
- Fire: Auto-generates CLI but less control over interface

---

## Decision 2: Data Validation

**Decision**: Pydantic V2

**Rationale**:
- Mandated by Constitution (Technical Constraints)
- Native Python dataclass-like syntax with validation
- Excellent error messages for validation failures
- Supports JSON serialization (useful for Phase II)
- V2 offers significant performance improvements

**Alternatives Considered**:
- attrs: Lighter weight but less validation features
- dataclasses: No built-in validation
- marshmallow: More verbose, schema-first approach

---

## Decision 3: Output Formatting

**Decision**: Rich library

**Rationale**:
- Mandated by Constitution (Principle IV: Rich CLI Human-Centered Interface)
- Beautiful tables, panels, and progress bars
- Color support for terminal output
- Error panels for graceful error display
- Consistent with "professional developer experience" goal

**Alternatives Considered**:
- tabulate: Tables only, no panels/colors
- colorama: Basic colors, no tables
- termcolor: Minimal formatting options

---

## Decision 4: Architecture Pattern

**Decision**: Service-Repository Pattern (3-layer)

**Rationale**:
- Mandated by Constitution (Principle II: Decoupled Service-Repository Architecture)
- Enables Phase II migration to PostgreSQL with zero service changes
- Clear separation of concerns:
  - **Repository**: Data access abstraction (InMemoryRepository for Phase I)
  - **Service**: Business logic and validation
  - **CLI**: User interface (Typer commands)

**Alternatives Considered**:
- Direct data access: Violates Constitution, tight coupling
- Active Record: Model contains persistence logic, harder to swap storage
- CQRS: Over-engineered for single-user Phase I

---

## Decision 5: ID Generation Strategy

**Decision**: Sequential integer IDs starting from 1

**Rationale**:
- Explicit in Spec Assumptions
- Simple and predictable for CLI usage
- Easy to reference in commands (`complete 1`, `delete 2`)
- Repository maintains counter internally

**Alternatives Considered**:
- UUID: Harder to type in CLI
- Timestamp-based: Not user-friendly
- Hash-based: Overkill for in-memory storage

---

## Decision 6: Testing Framework

**Decision**: pytest

**Rationale**:
- Industry standard for Python testing
- Excellent fixture support for repository mocking
- Parametrized tests for edge cases
- Integrates with `uv run pytest`

**Alternatives Considered**:
- unittest: More verbose, less flexible fixtures
- nose2: Less actively maintained
- hypothesis: Property-based testing (future consideration)

---

## Decision 7: Project Structure

**Decision**: Single project with `src/` layout

**Rationale**:
- Simple console app, no frontend/backend split needed
- Constitution requires modular separation (models, services, cli, repository)
- Tests in parallel `tests/` directory

**Structure**:
```
src/
├── todo/
│   ├── __init__.py
│   ├── models.py       # Pydantic models (Task)
│   ├── repository.py   # Repository interface + InMemoryRepository
│   ├── service.py      # TaskService (business logic)
│   └── cli.py          # Typer app with commands
└── __init__.py

tests/
├── unit/
│   ├── test_models.py
│   ├── test_repository.py
│   └── test_service.py
└── integration/
    └── test_cli.py
```

---

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Python version | 3.13+ (Constitution) |
| CLI framework | Typer (Constitution) |
| Validation | Pydantic V2 (Constitution) |
| Output formatting | Rich (Constitution) |
| Architecture | Service-Repository (Constitution) |
| Linting | Ruff (Constitution) |
| Package manager | uv (Constitution) |
| Testing | pytest (industry standard) |

---

## Next Steps

Proceed to Phase 1: Design data model and contracts.
