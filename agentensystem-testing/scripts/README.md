# Scripts Folder

Python automation scripts for the Agentic AI Testing pipeline. These are mechanical
helpers only — all validation, remediation, and quality judgment is performed by the
LLM (GitHub Copilot Chat) applying the skills in `.github/skills/`.

## Available Scripts

| Script | Purpose | LLM Required |
|--------|---------|--------------|
| `extract.py` | Convert input documents (PDF/DOCX/XLSX/VSDX) to markdown | No |
| `generate_context.py` | Bridge: export source + image inventory; the LLM authors the context (`export`) | Bridge only |
| `extract_requirements.py` | Bridge: export context/markdown; the LLM authors requirements; `build` writes Excel | Bridge only |
| `generate_test_cases.py` | Bridge: export requirements/context; the LLM authors tests; `build` writes Excel | Bridge only |
| `generate_traceability.py` | Build the requirement → test-case matrix | No |
| `llm_validate.py` | Mechanical bridge for LLM-driven validation/remediation (`export`/`report`/`remediate`) | Bridge only |
| `preflight_check.py` | Environment / prerequisite checks | No |
| `errors.py` | Shared exception classes (library, imported by other scripts) | No |

> Validation and remediation are LLM-driven. There are no deterministic scorer scripts;
> the previous `validate_requirements.py` / `validate_test_cases.py` / `remediate_*.py`
> scripts were removed in favor of `llm_validate.py` + the skills.

## Usage

```powershell
# Activate virtual environment first
.\.venv\Scripts\Activate.ps1

# Extract documents for a project
python scripts/extract.py --input inputs/JOVI --output output/extracted/JOVI

# Context generation bridge (LLM authors the context document)
python scripts/generate_context.py export --input output/extracted/JOVI --output output/generated_docs/JOVI_context_complete.md --project JOVI

# Requirements extraction bridge (LLM authors output/generated_docs/_llm_requirements.json, then build)
python scripts/extract_requirements.py export --project JOVI
# ... LLM writes output/generated_docs/_llm_requirements.json ...
python scripts/extract_requirements.py build --project JOVI

# Test-case generation bridge (LLM authors output/test_cases/_llm_test_cases.json, then build)
python scripts/generate_test_cases.py export --project_name JOVI
# ... LLM writes output/test_cases/_llm_test_cases.json ...
python scripts/generate_test_cases.py build --project_name JOVI

# LLM-driven validation bridge (requirements example)
python scripts/llm_validate.py export --artifact requirements
# ... LLM writes output/validation/_llm_verdict_requirements.json ...
python scripts/llm_validate.py report --verdict output/validation/_llm_verdict_requirements.json

# Generate traceability matrix
python scripts/generate_traceability.py
```
