# Track Plan: MVP - Beam Analysis Core & CLI

## Phase 1: Project Skeleton & Core Data Structures [checkpoint: dfbd087]
*Goal: Set up the project structure, dependency management, and define the core classes for Beam and Loads.*

- [x] Task: Initialize Poetry project and install dependencies (numpy, scipy, rich, inquirer, typer, pytest, black, flake8). a50a9ea
- [x] Task: Configure project settings (pyproject.toml, pytest.ini, linter configs). 4afb632
- [x] Task: Create `Load` base class and `PointLoad`, `UDL` subclasses (TDD: Write tests first for attributes and validation). 0317836
- [x] Task: Create `Beam` class with length and support properties (TDD: Write tests first for initialization and validation). 2fecafe
- [x] Task: Conductor - User Manual Verification 'Phase 1: Project Skeleton & Core Data Structures' (Protocol in workflow.md)

## Phase 2: Calculation Engine (Reactions & Internal Forces)
*Goal: Implement the physics engine to calculate reactions, shear, and moment arrays.*

- [x] Task: Implement `AnalysisEngine` class structure and dependency injection for Beam. e0f2b75
- [x] Task: Implement Reaction Force calculation for Point Loads (TDD: Test simple cases). c0fcbef
- [x] Task: Implement Reaction Force calculation for UDL (TDD: Test simple cases). 6c6f8de
- [x] Task: Implement Reaction Force calculation for combined loads (Superposition principle). 2c84fb8
- [x] Task: Implement Shear Force calculation logic (arrays/functions) (TDD: Verify V(x) values). d1e2f76
- [x] Task: Implement Bending Moment calculation logic (arrays/functions) (TDD: Verify M(x) values). 132c1f8
- [x] Task: Implement `get_max_shear` and `get_max_moment` helper methods. 3defc48
- [~] Task: Conductor - User Manual Verification 'Phase 2: Calculation Engine (Reactions & Internal Forces)' (Protocol in workflow.md)

## Phase 3: CLI Wizard & Input Handling
*Goal: Build the interactive command-line interface for data entry.*

- [ ] Task: Set up `typer` application entry point.
- [ ] Task: Implement `inquirer`/`rich` prompt for Beam Length input with validation.
- [ ] Task: Implement interactive loop for adding multiple Loads (Point/UDL).
- [ ] Task: Implement input summary display using `rich.table`.
- [ ] Task: Connect CLI inputs to the `Beam` and `AnalysisEngine` classes.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: CLI Wizard & Input Handling' (Protocol in workflow.md)

## Phase 4: Visualization & Reporting
*Goal: Display results and draw diagrams in the terminal.*

- [ ] Task: Implement Result Reporter module to display Reactions and Max values using `rich`.
- [ ] Task: Create ASCII Plotter utility for Shear Force Diagram (SFD) (Normalize data to terminal height/width).
- [ ] Task: Create ASCII Plotter utility for Bending Moment Diagram (BMD).
- [ ] Task: Integrate plotting into the main CLI flow.
- [ ] Task: Add color coding to diagrams (e.g., Red for negative, Green for positive, Bold for max values).
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Visualization & Reporting' (Protocol in workflow.md)

## Phase 5: Final Polish & Documentation
*Goal: Ensure code quality, add help documentation, and clean up.*

- [ ] Task: Refactor code for strict PEP 8 compliance and type hinting.
- [ ] Task: Write user documentation (Help command text).
- [ ] Task: Perform comprehensive integration test with a complex example problem.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Polish & Documentation' (Protocol in workflow.md)
