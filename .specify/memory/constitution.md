# Evolution of Todo Constitution

## Core Principles

### I. Spec-First Development (The Golden Rule)
No AI agent is permitted to generate or modify code without a referenced Task ID from `speckit.tasks`. Every feature must originate in `speckit.specify` and be architected in `speckit.plan` before execution. "Vibe coding" or manual coding is strictly prohibited.

### II. Decoupled Service-Repository Architecture
Even in Phase I (In-Memory), the business logic must be isolated from the storage layer. A Repository pattern must be used to ensure that moving from In-Memory (Phase I) to Neon PostgreSQL (Phase II) requires zero changes to the Core Service logic.

### III. Type-Safe Modern Python
All code must target Python 3.13+. Use of Type Hints, Pydantic V2 for data validation, and strict type checking is non-negotiable. Leverage Python 3.13's performance and typing improvements to ensure a robust system architected for AI-native scale.

### IV. Rich CLI Human-Centered Interface
Every command must produce human-readable, beautifully formatted output using the `Rich` library. Errors must be captured gracefully and reported via `Rich` panels to ensure a professional developer experience.

### V. Reusable Intelligence (Agent Skills)
Architecture must favor the creation of reusable Claude Code "Skills." Logic that can be abstracted into sub-agents or reusable automation scripts must be prioritized to secure bonus points for "Reusable Intelligence."

### VI. Test-Driven Verification
Implementation is only considered "Complete" when the implementation matches the Acceptance Criteria defined in `speckit.specify`. Automated verification of the CLI commands is required before moving to the next task.

## Technical Constraints
- **Language**: Python 3.13+
- **Environment**: WSL 2 (Windows Subsystem for Linux)
- **Dependency Management**: `uv` (Fast, reproducible builds)
- **CLI Framework**: `Typer`
- **Data Modeling**: `Pydantic`
- **Formatting/Linting**: `Ruff`

## Development Workflow
1. **Specify**: Update `speckit.specify` with the "What" and Acceptance Criteria.
2. **Plan**: Update `speckit.plan` with the "How" and Architectural Diagrams.
3. **Tasks**: Breakdown the plan into atomic, checkable tasks in `speckit.tasks`.
4. **Implement**: Use Claude Code to write code based on the approved tasks.
5. **Verify**: Run the code to ensure it meets the spec.

## Governance
This Constitution supersedes all other documentation and "implied" patterns. Any deviation from the Spec-Driven Development (SDD) cycle requires an amendment to this file. Claude Code is instructed to halt and request clarification if it detects a conflict between the current task and these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
