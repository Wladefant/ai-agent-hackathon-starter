# Copilot Instructions for Agentic AI in Testing

## Project Overview
Document Intelligence & Test Case Generator for processing project documents, extracting requirements, and generating validated test cases.

## Environment Setup - CRITICAL
Activate the virtual environment before running any Python scripts:

```powershell
if (-not (Test-Path ".venv")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Model Preferences
| Task | Model | Reason |
|------|-------|--------|
| Context Generation | Claude Opus 4 | Deep analysis, comprehensive synthesis |
| Requirements Extraction | Claude Opus 4 | Deep analysis, high-quality extraction |
| Requirements Validation | Claude Opus 4 | Thorough validation |
| Requirements Remediation | Claude Opus 4 | Intelligent fixes |
| Test Case Generation | Claude Opus 4 | Comprehensive coverage |
| Test Case Validation | Claude Opus 4 | Thorough QA |
| Test Case Remediation | Claude Opus 4 | Intelligent fixes |

**LLM Attribution:** All generated documents include a Metadata sheet with `LLM_Model: Claude Opus 4` and `Generated_Date`.

## Human Review Gates
The pipeline includes mandatory human approval points:
- **Gate 1:** After requirements extraction - approve extracted requirements
- **Gate 2:** After requirements validation - approve/remediate requirements
- **Gate 3:** After test case validation - approve/remediate test cases

## Domain Auto-Detection
The domain is automatically detected from input documents by analyzing file names, folder structure, document content keywords, and technical terminology patterns.

### Supported Domains (Auto-Detected)
| Domain | Detection Keywords |
|--------|-------------------|
| Core Banking/Payments | SEPA, SWIFT, ISO 20022, pacs, camt, IBAN, BIC, instant payment |
| Insurance | policy, claim, premium, underwriting, coverage |
| Lending | loan, mortgage, credit, disbursement, amortization |
| Trade Finance | LC, letter of credit, documentary, trade, export, import |
| Wealth Management | portfolio, investment, asset, custody, securities |
| Generic/IT | API, microservice, database, integration, REST |

### Domain Detection Logic
Domain is auto-detected from extracted markdown files in `output/extracted/` by scanning for domain-specific keywords and patterns. Falls back to "Generic/IT" if no specific domain is detected.

## Available Agents
- **@orchestrator** - Runs complete pipeline with human review gates. Usage: `@orchestrator Run the full pipeline for [PROJECT_NAME]`
- **@context_generator** - Uses Claude Opus 4 to analyze extracted documents and images. Output: `output/generated_docs/[project]_context_complete.md`
- **@requirements_extractor** - Extracts structured requirements using Claude Opus 4. Output: `output/generated_docs/extracted_requirements.xlsx`
- **@requirements_validator** - Validates and remediates requirements using Claude Opus 4. Output: `output/validation/requirements_validation_report.xlsx`
- **@test_case_generator** - Generates test cases using Claude Opus 4. Output: `output/test_cases/generated_test_cases.xlsx`
- **@test_case_validator** - Validates and remediates test cases using Claude Opus 4. Output: `output/validation/test_case_validation_report.xlsx`

## Available Skills
Skills can be invoked to enhance quality at various stages:

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `banking-domain-validator` | Apply Core Banking/Payments domain rules | Validating payment requirements |
| `requirements-quality-check` | INVEST criteria analysis | Before requirements approval |
| `test-case-quality-check` | Coverage and effectiveness analysis | Before test case approval |
| `intelligent-remediation` | Context-aware automated fixes | During remediation cycles |
| `human-review-preparation` | Generate review summaries | Before human gates |

## Folder Structure
- `inputs/` - Source documents (PDF, DOCX, XLSX, VSDX)
- `output/extracted/` - Markdown files (one per input)
- `output/generated_docs/` - Requirements Excel files, context documents
- `output/test_cases/` - Generated test cases
- `output/validation/` - Validation reports
- `output/traceability/` - Traceability matrix
- `output/remediation/` - Remediation logs
- `scripts/` - Python automation scripts
- `.github/agents/` - Agent definitions
- `.github/prompts/` - Dynamic prompt templates
- `.github/skills/` - Reusable skill definitions

## Scripts Usage
```powershell
.\.venv\Scripts\Activate.ps1
python scripts/extract.py --input inputs/JOVI --output output/extracted/JOVI
# Context generation is LLM-driven (see @context_generator); the bridge is:
python scripts/generate_context.py export --input output/extracted/JOVI --output output/generated_docs/JOVI_context_complete.md --project JOVI
# -> LLM reads output/generated_docs/_llm_input_context.json + images, authors the context .md
python scripts/extract_requirements.py export --project JOVI   # context+markdown -> JSON for the LLM
# -> LLM authors output/generated_docs/_llm_requirements.json
python scripts/extract_requirements.py build --project JOVI    # LLM JSON -> Excel workbook
# Requirements validation is LLM-driven (see @requirements_validator); the bridge is:
python scripts/llm_validate.py export --artifact requirements   # Excel -> JSON for LLM review
python scripts/llm_validate.py report --verdict output/validation/_llm_verdict_requirements.json  # verdict JSON -> report
# Test-case generation is LLM-driven (see @test_case_generator); the bridge is:
python scripts/generate_test_cases.py export --project_name JOVI   # requirements+context -> JSON for the LLM
# -> LLM authors output/test_cases/_llm_test_cases.json
python scripts/generate_test_cases.py build --project_name JOVI    # LLM JSON -> Excel workbook
# Test-case validation is LLM-driven (see @test_case_validator); the bridge is:
python scripts/llm_validate.py export --artifact test_cases
python scripts/llm_validate.py report --verdict output/validation/_llm_verdict_test_cases.json
python scripts/generate_traceability.py
```

## Workflow
Full Pipeline: `@orchestrator Run the full pipeline for JOVI`

Manual Steps: Extract → Context → Requirements → Validate Reqs → Test Cases → Validate TCs → Traceability

## Best Practices
1. Always activate `.venv` before Python operations
2. Place documents in project-specific subfolders under `inputs/`
3. Domain is auto-detected - no manual configuration needed
4. Extract documents before running agents
5. Review extracted requirements before validation
6. Generate context before test cases
7. Always validate generated test cases

## Constraints
- No embedding models available
- No LLM API access (use GitHub Copilot Chat for LLM operations)
- All processing is local and offline-capable
- Domain detection is keyword-based (no ML models)
