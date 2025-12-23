# Track Specification: MVP - Beam Analysis Core & CLI

## Overview
This track focuses on building the Minimum Viable Product (MVP) for the beam analysis CLI tool. The goal is to implement a robust calculation engine and a user-friendly CLI wizard that can handle simply supported beams with point loads and uniformly distributed loads (UDL). The output will include reaction forces, shear force diagrams (SFD), and bending moment diagrams (BMD) rendered in the terminal.

## Core Features
1.  **Simply Supported Beam Model:**
    -   Two supports: Pin (hinged) and Roller.
    -   Configurable beam length (meters).
    -   Validation: Length > 0, Support positions within beam limits.

2.  **Load Types:**
    -   **Point Load:** Force (kN) applied at a specific location.
    -   **Uniformly Distributed Load (UDL):** Force per unit length (kN/m) applied over the entire beam span.

3.  **Calculation Engine:**
    -   Calculate Support Reactions (Ra, Rb).
    -   Calculate Shear Force values along the beam.
    -   Calculate Bending Moment values along the beam.
    -   Identify critical values: Max Shear, Max Moment.

4.  **CLI Interface:**
    -   Interactive wizard using `inquirer` or `rich.prompt`.
    -   Step-by-step data entry: Beam properties -> Loads -> Analyze.
    -   Input validation with helpful error messages.

5.  **Visualization & Reporting:**
    -   Terminal-based output using `rich`.
    -   Summary table of input data.
    -   Summary table of results (Reactions, Max V, Max M).
    -   ASCII-based plotting for SFD and BMD.

## Technical Requirements
-   **Language:** Python 3.10+
-   **Libraries:** `numpy`, `scipy`, `rich`, `inquirer`, `typer`.
-   **Testing:** `pytest` with >80% coverage.
-   **Architecture:** Modular design separating `Beam`, `Load`, `AnalysisEngine`, and `CLI` components.

## User Flow
1.  User starts the tool via CLI command.
2.  Wizard asks for Beam Length.
3.  Wizard asks to add loads (Point or UDL) iteratively.
4.  User confirms to start analysis.
5.  Tool displays input summary.
6.  Tool calculates and displays Reaction Forces.
7.  Tool displays Shear Force Diagram (ASCII) + Max V.
8.  Tool displays Bending Moment Diagram (ASCII) + Max M.
