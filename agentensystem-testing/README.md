# Agentic AI in Testing — Document Intelligence & Test Case Generator

An agent-driven platform that turns project documentation into validated requirements and test cases. It processes multi-format documents (PDF, DOCX, PPTX, VSDX, XLSX, TXT, MD), auto-detects the business domain, and runs a gated pipeline orchestrated by GitHub Copilot agents. Visio diagrams are read **as flows** — shapes and their connectors are reconstructed into a directed graph (Mermaid flowchart + branch-labelled steps + swimlanes), not just a flat list of labels.

## Architecture: LLM-Driven Bridges

This platform uses a **bridge architecture**. Python scripts perform only mechanical I/O; **all judgment, scoring, and authoring is done by the LLM** (GitHub Copilot — Claude Opus 4) applying the skill files in `.github/skills/`.

```
export (Excel/source → JSON)  →  LLM reads JSON + skills, authors result JSON  →  build/report (JSON → Excel)
```

No deterministic scorers, no hardcoded test bodies, no embedding models, no cloud APIs. Every stage is local and offline-capable.

## Folder Structure

```
├── .github/
│   ├── agents/          # Agent definitions (orchestrator, extractors, validators, generators)
│   ├── prompts/         # Dynamic prompt templates
│   └── skills/          # Reusable skill definitions applied by the LLM
├── inputs/              # Source documents, organized by project (e.g. inputs/JOVI/)
├── output/              # All generated artifacts (parent folder)
│   ├── extracted/       # Markdown files (one per input document) + image inventories
│   ├── generated_docs/  # Context, requirements, execution summary
│   ├── test_cases/      # Generated test cases
│   ├── validation/      # Validation reports
│   ├── traceability/    # Traceability matrix
│   └── remediation/     # Remediation logs
├── scripts/             # Python automation bridges
├── config.json          # Single source of truth (paths, models, thresholds)
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Quick Start

```powershell
# 1. Create & activate the virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add documents to inputs/[PROJECT_NAME]/  (e.g. inputs/JOVI/)
```

> Windows note: the console defaults to cp1252. Prefix Python commands with `$env:PYTHONIOENCODING="utf-8"` to avoid encoding errors on glyph output.

## Running the Pipeline

### Option A — Full Automated Pipeline (Recommended)
```
@orchestrator Run the full pipeline for JOVI
```
The orchestrator runs every stage and pauses at the human review gates.

### Option B — Manual Step-by-Step

```powershell
# 1. Extract documents to markdown (auto-detects domain)
python scripts/extract.py --input inputs/JOVI --output output/extracted/JOVI

# 2. Generate context (LLM-driven bridge)
python scripts/generate_context.py export --input output/extracted/JOVI --output output/generated_docs/JOVI_context_complete.md --project JOVI
#   → @context_generator reads output/generated_docs/_llm_input_context.json + images, authors the context .md

# 3. Extract requirements (LLM-driven bridge)
python scripts/extract_requirements.py export --project JOVI
#   → @requirements_extractor authors output/generated_docs/_llm_requirements.json
python scripts/extract_requirements.py build --project JOVI

# --- GATE 1: Approve extracted requirements ---

# 4. Validate requirements (LLM-driven bridge)
python scripts/llm_validate.py export --artifact requirements
#   → @requirements_validator writes output/validation/_llm_verdict_requirements.json
python scripts/llm_validate.py report --verdict output/validation/_llm_verdict_requirements.json

# --- GATE 2: Approve / remediate requirements ---
#   (optional) remediate:
python scripts/llm_validate.py remediate --patch output/validation/_llm_remediation_requirements.json

# 5. Generate test cases (LLM-driven bridge)
python scripts/generate_test_cases.py export --project_name JOVI
#   → @test_case_generator authors output/test_cases/_llm_test_cases.json
python scripts/generate_test_cases.py build --project_name JOVI

# 6. Validate test cases (LLM-driven bridge)
python scripts/llm_validate.py export --artifact test_cases
#   → @test_case_validator writes output/validation/_llm_verdict_test_cases.json
python scripts/llm_validate.py report --verdict output/validation/_llm_verdict_test_cases.json

# --- GATE 3: Approve / remediate test cases ---

# 7. Generate traceability matrix
python scripts/generate_traceability.py
```

## Human Review Gates

The pipeline pauses at three mandatory approval points:

| Gate | After | Decision |
|------|-------|----------|
| **Gate 1** | Requirements extraction | Approve extracted requirements |
| **Gate 2** | Requirements validation | Approve or remediate requirements |
| **Gate 3** | Test case validation | Approve or remediate test cases |

## Model Preferences

All judgment stages use **Claude Opus 4** for deep analysis and high-quality output. Every generated artifact includes a Metadata sheet with `LLM_Model: Claude Opus 4` and `Generated_Date`.

| Task | Model |
|------|-------|
| Context Generation | Claude Opus 4 |
| Requirements Extraction / Validation / Remediation | Claude Opus 4 |
| Test Case Generation / Validation / Remediation | Claude Opus 4 |

## Agents

| Agent | Purpose |
|-------|---------|
| `@orchestrator` | Runs the complete pipeline with human review gates |
| `@context_generator` | Reads extracted docs + images, authors the context document |
| `@requirements_extractor` | Extracts structured requirements |
| `@requirements_validator` | Validates and remediates requirements (LLM scoring) |
| `@test_case_generator` | Authors test cases from requirements + context |
| `@test_case_validator` | Validates and remediates test cases (LLM scoring) |

## Skills

Skills package domain knowledge that the LLM opens and applies at each stage:

| Skill | Purpose |
|-------|---------|
| `banking-domain-validator` | Core Banking / Payments domain rules |
| `requirements-quality-check` | INVEST-criteria analysis |
| `test-case-quality-check` | Coverage and effectiveness analysis |
| `intelligent-remediation` | Context-aware automated fixes |
| `human-review-preparation` | Review summaries for the gates |

## Prompt Templates

Each authoring/validation agent loads a matching template from `.github/prompts/`. The
template supplies the detailed structure, field rules, and scoring rubric; the agent
definition stays the source of truth where they differ (validators let the prompt take
precedence).

| Prompt | Used by |
|--------|---------|
| `context-generation.prompt.md` | `@context_generator` |
| `requirements-extraction.prompt.md` | `@requirements_extractor` |
| `requirements-validation.prompt.md` | `@requirements_validator` |
| `test-case-generation.prompt.md` | `@test_case_generator` |
| `test-case-validation.prompt.md` | `@test_case_validator` |

All prompts share the same verdict rule as the bridge: **PASS** = all dimensions ≥ 4,
**FAIL** = any dimension < 3, else **SOFT-FAIL**.

## Domain Auto-Detection

The domain is detected automatically from the extracted markdown by scanning for domain-specific keywords. Falls back to **Generic/IT** if none match.

| Domain | Detection Keywords |
|--------|-------------------|
| Core Banking/Payments | SEPA, SWIFT, ISO 20022, pacs, camt, IBAN, BIC, instant payment |
| Insurance | policy, claim, premium, underwriting, coverage |
| Lending | loan, mortgage, credit, disbursement, amortization |
| Trade Finance | LC, letter of credit, documentary, export, import |
| Wealth Management | portfolio, investment, asset, custody, securities |
| Generic/IT | API, microservice, database, integration, REST |

## Scripts

| Script | Role |
|--------|------|
| `extract.py` | Convert documents to markdown + image inventory; detect domain |
| `generate_context.py` | Context bridge (`export` → LLM authors `.md`) |
| `extract_requirements.py` | Requirements bridge (`export` → LLM authors JSON → `build`) |
| `generate_test_cases.py` | Test-case bridge (`export` → LLM authors JSON → `build`) |
| `llm_validate.py` | Validation/remediation bridge (`export` / `report` / `remediate`) |
| `generate_traceability.py` | Build the requirements ↔ test case traceability matrix |
| `preflight_check.py` | Pre-run environment / input checks |
| `errors.py` | Shared error types (`ProjectError`, `FileOperationError`) |

## Supported Document Formats

| Format | Extension | Method |
|--------|-----------|--------|
| PDF | `.pdf` | PyPDF text extraction |
| Word | `.docx` | python-docx |
| PowerPoint | `.pptx` | python-pptx |
| Excel | `.xlsx` | openpyxl |
| Visio | `.vsdx` | Structured flow graph: shapes + connectors → Mermaid flowchart, branch-labelled steps & swimlanes |
| Text / Markdown | `.txt` / `.md` | Direct read / pass-through |

## Output Artifacts

| File | Contents |
|------|----------|
| `output/generated_docs/{project}_context_complete.md` | Consolidated, LLM-authored project context |
| `output/generated_docs/extracted_requirements.xlsx` | Structured requirements (active + merged duplicates) |
| `output/validation/requirements_validation_report.xlsx` | Per-requirement scoring & verdict |
| `output/test_cases/generated_test_cases.xlsx` | Test suite (Test_Cases, Coverage_Matrix, Summary, Metadata) |
| `output/validation/test_case_validation_report.xlsx` | Per-test-case scoring & verdict |
| `output/traceability/traceability_matrix.xlsx` | Requirements → test case coverage |
| `output/generated_docs/pipeline_execution_summary.md` | End-to-end run summary |

**Scoring dimensions** — Requirements: Completeness, Clarity, Testability, Traceability. Test Cases: Traceability, Clarity, Completeness. Verdicts: **PASS** (all dims ≥ 4), **SOFT-FAIL** (all ≥ 3), **FAIL** (otherwise). Duplicate requirements are flagged `Status = MERGED` (excluded from pass-rate, not renumbered).

## Reference Run — JOVI

JOVI (ING FI Instant SEPA Payments engine, Core Banking/Payments domain) completed end-to-end with **zero FAIL** verdicts:

| Stage | Result |
|-------|--------|
| Requirements | 135 total → 112 active, 23 merged · 70 PASS / 42 SOFT-FAIL / 0 FAIL |
| Test Cases | 228 generated · 100% active-requirement coverage · 213 PASS / 15 SOFT-FAIL / 0 FAIL |
| Traceability | 94.1% · PASS |

## Requirements

- **Python 3.10+** (developed/tested on 3.14)
- Windows, macOS, or Linux
- Dependencies: see `requirements.txt` (`pypdf`, `python-docx`, `python-pptx`, `openpyxl`, …)

No cloud API keys, no model downloads, no embedding models — all processing is local and private.

## Troubleshooting

| Issue | Resolution |
|-------|-----------|
| `No module named '...'` | `pip install -r requirements.txt` (with `.venv` activated) |
| `UnicodeEncodeError` on glyphs | Prefix commands with `$env:PYTHONIOENCODING="utf-8"` |
| `PermissionError` saving Excel | Close the workbook in Excel/preview before re-running |
| Re-running remediation | Restore `*.pre_remediation.xlsx` before re-applying a patch (remediate backs up at start of each run) |
| Low domain confidence | Add more domain-specific documents; ensure content is text (not scanned images) |

## Best Practices

1. Always activate `.venv` before Python operations.
2. Place documents in project-specific subfolders under `inputs/`.
3. Extract documents before running agents; generate context before test cases.
4. Let domain auto-detection work — no manual configuration needed.
5. Use the review gates to catch issues early; always validate generated test cases.
