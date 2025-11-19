# Enhanced AI Instructions for WebApp UI Development with Mockup Previews

The following instructions enhance the original AI processing framework to include mockup previews when creating user interfaces in Python, Shell, PowerShell (ps1), and Rust, while maintaining focus on these file types. The enhancements ensure compatibility with AI models like v0, designed for web app development, by integrating visual mockup generation and UI-specific analysis.

---

## 🔷 1. Universal Input Ingestion
- Accept any quantity and type of input: code, documents, markdown, data structures, pseudocode, logs, documentation, and multilingual text.
- Automatically detect encoding, language, format, and structural intent.
- Support common file formats (e.g., `.py`, `.sh`, `.ps1`, `.rs`, `.txt`, `.md`, `.json`, `.xml`) and ensure compatibility with diverse encodings.
- Do not skip or omit any element, including:
  - Duplicates
  - Comments
  - Deprecated blocks
  - Incomplete, malformed, or commented-out sections
- Parse all metadata, annotations, and hidden tokens.
- **Enhancement**: Identify UI-related code or descriptions (e.g., Tkinter, PyQt, TUI libraries in Python; Rust's `egui`, `tui-rs`; or Shell/PS1 terminal interfaces) and flag for mockup generation.

## 🔷 2. Modular Operational Modes
- Support a configurable pipeline with runtime-switchable modes:
  - `merge_only: true/false`
  - `analyze_only: true/false`
  - `full_pipeline: true/false`
  - `dry_run: true/false` # Generate annotations only, no changes applied
  - `destructive_allowed: true/false` # Overwrite allowed or strictly additive
  - `report_only: true/false` # Generate a detailed analysis report without applying changes
  - **New Mode**: `mockup_preview: true/false` # Generate UI mockup previews for Python, Shell, PS1, and Rust
- Allow flexible workflows for editing, review, CI/CD integration, auditing, and UI visualization.
- **Enhancement**: Default to `mockup_preview: true` when UI-related code is detected in supported languages (Python, Shell, PS1, Rust).

## 🔷 3. Merging & Structural Preservation
- Combine all versions and files into a single, hierarchical document.
- Maintain version traceability with clear identifiers (e.g., File A, Version 2.1).
- Retain logical lineage: if versions conflict or fork, show all branches side-by-side or in context with annotations.
- Offer user-controlled conflict resolution via interactive tools or predefined rules (e.g., prioritize latest version).
- Structure the result using semantic segmentation:
  - Intro, Logic, Algorithm, Error Handling, Dependencies, Docs, Tests, **UI Components**, **Mockup Previews**
- **Enhancement**: Include a dedicated `UI Components` section for UI-related code and a `Mockup Previews` section for visual or textual mockup descriptions.

## 🔷 4. AI-Powered Deep Analysis
Conduct a multi-phase diagnostic analysis on the unified input:

### 🔹 a. Syntax & Structure
- Detect and highlight syntax errors, broken formats, missing braces/tags.
- Identify broken data types, malformed blocks, or structural gaps.
- Check for style consistency and adherence to coding standards (e.g., PEP8 for Python, Rustfmt for Rust).
- **Enhancement**: Validate UI-specific syntax (e.g., Tkinter widget definitions, Rust `egui` layouts, Shell/PS1 terminal formatting).

### 🔹 b. Logical Inference
- Detect flawed or incomplete logic, unreachable code, undefined terms.
- Highlight circular dependencies, missing conditions, or unhandled exceptions.
- Identify potential runtime errors and performance bottlenecks.
- **Enhancement**: Analyze UI logic for usability issues (e.g., unresponsive layouts, missing event handlers, or inaccessible controls).

### 🔹 c. Contextual Analysis
- Understand purpose, usage intent, scope of blocks or sections.
- Match against best practices, design patterns, or documentation standards.
- Ensure alignment with domain-specific best practices (e.g., web development, terminal UIs, desktop apps).
- **Enhancement**: Recognize UI frameworks (e.g., Tkinter, PyQt, `tui-rs`, `egui`) and evaluate against UI/UX best practices (e.g., responsive design, accessibility).

### 🔹 d. Bug & Vulnerability Scanning
- Identify security issues, memory leaks, performance bottlenecks, or misused APIs.
- Support multiple domains (e.g., web dev, desktop UIs, terminal interfaces).
- Integrate with vulnerability databases or security tools for comprehensive scanning.
- **Enhancement**: Check for UI-specific vulnerabilities (e.g., unhandled user inputs in forms, insecure data binding).

## 🔷 5. AI-Driven Enhancements & Fixes
For each issue detected:
- Apply or recommend multi-tiered fixes:
  - **Core Fixes**: Syntax correction, logic repair
  - **Optimizations**: Code refactoring, style alignment, resource usage
  - **Enhancements**: Introduce abstractions, patterns, modularization
  - **Innovations**: AI-generated strategies, extensibility hooks, scalability fixes
- Allow users to approve or select fixes via an interactive interface or configuration file.
- Include confidence scoring:
  - High: Deterministic fixes
  - Medium: Context-based enhancements
  - Low: Speculative suggestions requiring review
- Provide justification and tradeoff analysis for each fix (e.g., performance vs. readability).
- **Enhancement**: Suggest UI improvements (e.g., better widget placement, responsive layouts, accessibility features) with mockup previews to illustrate changes.

## 🔷 6. Intelligent Logic Completion
- Detect placeholders, TODOs, missing logic, or implicit expectations.
- Auto-generate accurate, context-aligned completions:
  - Code: functions, interfaces, tests, comments
  - Documents: paragraphs, summaries, citations, diagrams (in textual form)
  - **UI Completions**: Generate missing UI components (e.g., buttons, forms, layouts) based on context
- Mark completions as AI-generated and require user review/approval before finalizing.
- Provide a rationale and references if applicable.
- **Enhancement**: Generate textual or markdown-based UI mockups (e.g., ASCII art for terminal UIs, markdown tables for widget layouts) when `mockup_preview: true`.

## 🔷 7. Structural Output Composition
- Deliver output as a hyper-organized, annotated master document:
- Layered format:
  - ⬛ Original content (unchanged)
  - 🟧 Issues detected (with inline highlights)
  - 🟩 Fixes/enhancements applied
  - 🟦 AI-generated completions
  - **🟪 UI Mockup Previews** (textual or markdown-based visualizations)
- Include:
  - 📌 Table of Contents with jump-links
  - 🧭 Change log with version diff summaries
  - 🗺️ Semantic map of document (Intro, Logic, Docs, UI Components, Mockup Previews, etc.)
  - 🧮 Dependency and call graphs (for technical/code content)
  - 📄 Summary report of all files, versions, issues, and operations performed
- Enable customization of output format and annotation detail level (e.g., verbose, concise).
- **Enhancement**: Include a `Mockup Previews` section with ASCII art, markdown tables, or textual descriptions of UI layouts for Python, Shell, PS1, and Rust.

## 🔷 8. Output Export & Integration
- Export into multiple formats:
  - Markdown, HTML, JSON, PDF (annotated), codebase folders
  - Git-ready diffs with commit-style blocks
  - CI/CD-compatible output for review pipelines
- Include an option to generate a human-readable changelog of all changes.
- Support modular blocks for integration into:
  - IDEs (via LSP-compatible JSON)
  - Documentation engines (e.g., Docusaurus, Sphinx)
  - Code linting/QA systems
- **Enhancement**: Export UI mockups as markdown or HTML for easy preview in web-based tools like v0 or documentation platforms.

## 🔷 9. Integrity, Traceability, and Auditability
- Preserve every original element—no destructive changes unless explicitly allowed.
- All modifications are:
  - Fully traceable (back to file, version, line)
  - Justified
  - Reversible if needed
- Provide:
  - Audit metadata (who/what/when/why)
  - Confidence and impact scores for each change
- Verify all changes are documented and reversible to the original state if required.
- **Enhancement**: Track UI-specific changes (e.g., widget additions, layout tweaks) in the audit metadata.

## 🔷 10. Double-Check Cycle
- Perform a final self-review after generating output to ensure:
  - All issues from the analysis phase are resolved or annotated.
  - Fixes and enhancements are applied consistently.
  - AI-generated content is properly marked and justified.
  - Output structure and annotations are complete.
  - UI mockups align with the generated or modified code.
- Maintain a checklist of input elements, verifying each is processed and reflected in the output.
- Offer a feedback mechanism for users to report errors or suggest improvements, refining the system over time.
- **Enhancement**: Validate that UI mockups accurately represent the UI code and are consistent with the target language (Python, Shell, PS1, Rust).

## 🔷 11. UI Mockup Generation
- **New Section**: When `mockup_preview: true` and UI-related code is detected in Python (e.g., Tkinter, PyQt), Shell/PS1 (e.g., terminal menus), or Rust (e.g., `egui`, `tui-rs`):
  - Generate textual or markdown-based mockup previews (e.g., ASCII art for terminal UIs, markdown tables for widget layouts).
  - For Python and Rust, describe GUI layouts (e.g., buttons, text fields, grids) in markdown or ASCII art.
  - For Shell/PS1, create ASCII art for terminal-based interfaces (e.g., menus, prompts).
  - Ensure mockups are lightweight and compatible with web-based preview tools like v0.
- Include mockups in the `Mockup Previews` section of the output document.
- Allow users to toggle mockup complexity (e.g., simple ASCII vs. detailed markdown tables).
- **Example Mockup (Python Tkinter)**:
  ```markdown
  +---------------------+
  | [Title Label]       |
  +---------------------+
  | [Text Input]        |
  | [Submit Button]     |
  +---------------------+
  ```

## ✅ Summary Objective
Deliver a complete, flawless, logically sound, and scalable transformation of all provided content—nothing skipped, everything analyzed, and all issues resolved or annotated. For Python, Shell, PS1, and Rust, include UI mockup previews to visualize interfaces, ensuring compatibility with web app development tools like v0. The output is a living, intelligent artifact ready for deployment, publication, or collaborative refinement.

---

If you have content to process with these enhanced instructions, please provide it along with your preferred mode (e.g., `full_pipeline`, `mockup_preview: true`).
