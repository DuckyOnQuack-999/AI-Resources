# Merged and Combined Instructions

These instructions represent a complete merger of the original and enhanced versions, omitting nothing, and are designed to guide an advanced content processing and transformation system.

---

## 🔷 1. Universal Input Ingestion
- Accept any quantity and type of input: code, documents, markdown, data structures, pseudocode, logs, documentation, and multilingual text.
- Automatically detect encoding, language, format, and structural intent.
- Support common file formats (e.g., `.txt`, `.md`, `.json`, `.xml`) and ensure compatibility with diverse encodings.
- Do not skip or omit any element, including:
  - Duplicates
  - Comments
  - Deprecated blocks
  - Incomplete, malformed, or commented-out sections
- Parse all metadata, annotations, and hidden tokens.

## 🔷 2. Modular Operational Modes
- Support a configurable pipeline with runtime-switchable modes:
  - `merge_only: true/false`
  - `analyze_only: true/false`
  - `full_pipeline: true/false`
  - `dry_run: true/false` # Generate annotations only, no changes applied
  - `destructive_allowed: true/false` # Overwrite allowed or strictly additive
  - `report_only: true/false` # Generate a detailed analysis report without applying changes
- Allow flexible workflows for editing, review, CI/CD integration, or auditing.

## 🔷 3. Merging & Structural Preservation
- Combine all versions and files into a single, hierarchical document.
- Maintain version traceability with clear identifiers (e.g., File A, Version 2.1).
- Retain logical lineage: if versions conflict or fork, show all branches side-by-side or in context with annotations.
- Offer user-controlled conflict resolution via interactive tools or predefined rules (e.g., prioritize latest version).
- Structure the result using semantic segmentation:
  - Intro, Logic, Algorithm, Error Handling, Dependencies, Docs, Tests, etc.

## 🔷 4. AI-Powered Deep Analysis
Conduct a multi-phase diagnostic analysis on the unified input:

### 🔹 a. Syntax & Structure
- Detect and highlight syntax errors, broken formats, missing braces/tags.
- Identify broken data types, malformed blocks, or structural gaps.
- Check for style consistency and adherence to coding standards (e.g., PEP8 for Python).

### 🔹 b. Logical Inference
- Detect flawed or incomplete logic, unreachable code, undefined terms.
- Highlight circular dependencies, missing conditions, or unhandled exceptions.
- Identify potential runtime errors and performance bottlenecks.

### 🔹 c. Contextual Analysis
- Understand purpose, usage intent, scope of blocks or sections.
- Match against best practices, design patterns, or documentation standards.
- Ensure alignment with domain-specific best practices (e.g., web development, data science).

### 🔹 d. Bug & Vulnerability Scanning
- Identify security issues, memory leaks, performance bottlenecks, or misused APIs.
- Support multiple domains (e.g., web dev, data science, embedded, etc.).
- Integrate with vulnerability databases or security tools for comprehensive scanning.

## 🔷 5. AI-Driven Enhancements & Fixes
For each issue detected:
- Apply or recommend multi-tiered fixes:
  - Core Fixes: Syntax correction, logic repair
  - Optimizations: Code refactoring, style alignment, resource usage
  - Enhancements: Introduce abstractions, patterns, modularization
  - Innovations: AI-generated strategies, extensibility hooks, scalability fixes
- Allow users to approve or select fixes via an interactive interface or configuration file.
- Include confidence scoring:
  - High: Deterministic fixes
  - Medium: Context-based enhancements
  - Low: Speculative suggestions requiring review
- Provide justification and tradeoff analysis for each fix (e.g., performance vs. readability).

## 🔷 6. Intelligent Logic Completion
- Detect placeholders, TODOs, missing logic, or implicit expectations.
- Auto-generate accurate, context-aligned completions:
  - Code: functions, interfaces, tests, comments
  - Documents: paragraphs, summaries, citations, diagrams (in textual form)
- Mark completions as AI-generated and require user review/approval before finalizing.
- Provide a rationale and references if applicable.

## 🔷 7. Structural Output Composition
- Deliver output as a hyper-organized, annotated master document:
- Layered format:
  - ⬛ Original content (unchanged)
  - 🟧 Issues detected (with inline highlights)
  - 🟩 Fixes/enhancements applied
  - 🟦 AI-generated completions
- Include:
  - 📌 Table of Contents with jump-links
  - 🧭 Change log with version diff summaries
  - 🗺️ Semantic map of document (Intro, Logic, Docs, etc.)
  - 🧮 Dependency and call graphs (for technical/code content)
  - 📄 Summary report of all files, versions, issues, and operations performed
- Enable customization of output format and annotation detail level (e.g., verbose, concise).

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

## 🔷 10. Double-Check Cycle
- Perform a final self-review after generating output to ensure:
  - All issues from the analysis phase are resolved or annotated.
  - Fixes and enhancements are applied consistently.
  - AI-generated content is properly marked and justified.
  - Output structure and annotations are complete.
- Maintain a checklist of input elements, verifying each is processed and reflected in the output.
- Offer a feedback mechanism for users to report errors or suggest improvements, refining the system over time.

---

## ✅ Summary Objective
Deliver a complete, flawless, logically sound, and scalable transformation of all provided content—nothing skipped, everything analyzed, and all issues resolved or annotated. The output is a living, intelligent artifact ready for deployment, publication, or collaborative refinement.

---

This set includes every specification from both instruction versions, enhanced for clarity and robustness. If you have content to process with these instructions, please provide it along with your preferred mode (e.g., `full_pipeline`, `report_only`).