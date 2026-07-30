---
name: orchestrator
description: Runs complete document-to-test-case pipeline with human review gates
---

# Orchestrator Agent

## Precedence Rule
If any section conflicts, follow **Workflow Steps 0–14** as the sole source of truth. Behavior Guidelines and Diagrams are illustrative only.

## Purpose
Execute the full pipeline in this exact order:
0. Cleanup Previous Outputs
1. Environment Setup
2. Document Extraction
3. Context Generation
4. Requirements Extraction
5. 🛑 HUMAN REVIEW GATE 1 (Requirements Approval)
6. Requirements Validation
7. Requirements Remediation (if needed)
8. 🛑 HUMAN REVIEW GATE 2 (Validation Approval)
9. Test Case Generation
10. Test Case Validation
11. Test Case Remediation (if needed)
12. 🛑 HUMAN REVIEW GATE 3 (Test Case Approval)
13. Traceability Generation
14. Pipeline Summary

## Available Skills (active — load and apply, don't just reference)
Skills are domain knowledge files in `.github/skills/`. They are "active" only when
the responsible agent OPENS the file and applies its rules. Each validation/review
step below must read the linked skill(s) before producing output.

| Skill | Load at step | Link |
|-------|-------------|------|
| `requirements-quality-check` | Step 6 (req validation) | [file](../skills/requirements-quality-check.skill.md) |
| `test-case-quality-check` | Step 9 (TC validation) | [file](../skills/test-case-quality-check.skill.md) |
| `banking-domain-validator` | Steps 6, 9 (domain checks) | [file](../skills/banking-domain-validator.skill.md) |
| `intelligent-remediation` | Steps 7, 10 (remediation) | [file](../skills/intelligent-remediation.skill.md) |
| `human-review-preparation` | Gates 1, 2, 3 | [file](../skills/human-review-preparation.skill.md) |

## Validation is LLM-driven (not Python-scored)
Requirements and test-case validation are performed by the LLM applying the skills
above. Python's role is limited to the mechanical I/O bridge `scripts/llm_validate.py`
(`export` artifact → JSON; `report` verdict-JSON → Excel; `remediate` patch → Excel).
The legacy deterministic scorers have been REMOVED; do not reintroduce Python scoring.

## Preflight Checks
Before Step 1, verify:
- `inputs/` or `docs/` contains at least one supported file (.pdf, .docx, .xlsx, .vsdx, .md)
- `python --version` >= 3.8
- `.venv` directory exists or can be created

If any check fails, stop and report the exact missing prerequisite.

## Workflow Steps

### Step 0: Cleanup Previous Outputs
Clean all generated and extracted documents from previous runs:
```powershell
# Clean extracted documents
if (Test-Path "output/extracted/") { Remove-Item -Path "output/extracted/*" -Recurse -Force -ErrorAction SilentlyContinue }
# Clean generated documents
if (Test-Path "output/generated_docs/") { Remove-Item -Path "output/generated_docs/*" -Recurse -Force -ErrorAction SilentlyContinue }
# Clean test cases
if (Test-Path "output/test_cases/") { Remove-Item -Path "output/test_cases/*" -Recurse -Force -ErrorAction SilentlyContinue }
# Clean validation reports
if (Test-Path "output/validation/") { Remove-Item -Path "output/validation/*" -Recurse -Force -ErrorAction SilentlyContinue }
# Clean traceability
if (Test-Path "output/traceability/") { Remove-Item -Path "output/traceability/*" -Recurse -Force -ErrorAction SilentlyContinue }
# Clean remediation logs
if (Test-Path "output/remediation/") { Remove-Item -Path "output/remediation/*" -Recurse -Force -ErrorAction SilentlyContinue }
Write-Host "✅ Cleaned previous outputs"
```

### Step 1: Environment Setup (Run Once)
```powershell
if (-not (Test-Path ".venv")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Run Step 1 once at start; do not repeat unless shell resets.

### Step 2: Document Extraction
Extract all input documents to markdown:
```powershell
python scripts/extract.py --input inputs/${project_name} --output output/extracted/${project_name}
```
Output: `output/extracted/${project_name}/*.md` and `output/extracted/${project_name}/${project_name}_extraction_manifest.json`

### Step 3: Context Generation
Invoke `@context_generator` to synthesize a comprehensive context document.

The context generator will:
1. Run `python scripts/generate_context.py export --input output/extracted/${project_name} --output output/generated_docs/${project_name}_context_complete.md --project ${project_name}` to prepare the source bundle (`output/generated_docs/_llm_input_context.json`)
2. Read all source documents and VIEW all inventoried images/diagrams
3. Author (LLM synthesis) a comprehensive context document and write it to the output path
4. Output detailed technical specifications, business processes, and test-relevant details

Output: `output/generated_docs/{project_name}_context_complete.md`

### Step 3.5: Generate Validation Context
Create `output/generated_docs/validation_context.json` with project metadata for downstream validation:
```powershell
$manifest = Get-Content "output/extracted/${project_name}/${project_name}_extraction_manifest.json" -ErrorAction SilentlyContinue | ConvertFrom-Json
$domain = if ($manifest.detected_domain) { $manifest.detected_domain } else { "Generic/IT" }

$context = @{
    project_name = "${project_name}"
    domain = $domain
    context_file = "output/generated_docs/${project_name}_context_complete.md"
    requirements_file = "output/generated_docs/extracted_requirements.xlsx"
    test_cases_file = "output/test_cases/generated_test_cases.xlsx"
    generated_date = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
}
$context | ConvertTo-Json -Depth 3 | Out-File "output/generated_docs/validation_context.json" -Encoding utf8
Write-Host "✅ Created validation_context.json"
```
Output: `output/generated_docs/validation_context.json`

### Step 4: Requirements Extraction
Invoke `@requirements_extractor` for the project.
Uses the context document and extracted markdown files to identify requirements.
Output: `output/generated_docs/extracted_requirements.xlsx`

### Step 5: 🛑 HUMAN REVIEW GATE 1
Present extracted requirements for review:
```
══════════════════════════════════════════════════════════
🛑 HUMAN REVIEW GATE 1: Requirements Extraction Review
══════════════════════════════════════════════════════════
File: output/generated_docs/extracted_requirements.xlsx
Action Required: APPROVE | REJECT
════════════════════════════════════════════════════════════
```
- If APPROVE: proceed to Step 6
- If REJECT: terminate pipeline immediately, write `output/generated_docs/pipeline_execution_summary.md` with status = "Stopped by reviewer at Gate 1"

### Step 6: Requirements Validation (LLM-driven)
Invoke `@requirements_validator`. The agent loads the requirements-quality-check +
banking-domain-validator skills, judges each requirement with the LLM, and persists
the report via `scripts/llm_validate.py`.
Output: `output/validation/requirements_validation_report.xlsx`

### Step 7: 🛑 HUMAN REVIEW GATE 2
Present validation results:
```
══════════════════════════════════════════════════════════
🛑 HUMAN REVIEW GATE 2: Requirements Validation Review
══════════════════════════════════════════════════════════
File: output/validation/requirements_validation_report.xlsx
Quality Gate Status: PASS_RATE = (PASS / total) * 100, rounded to 1 decimal
VERDICT_COUNT format: PASS:x, SOFT-FAIL:y, FAIL:z
Action Required: APPROVED | PROCEED | REMEDIATE
══════════════════════════════════════════════════════════
```
- If APPROVED/PROCEED: continue to Step 8
- If REMEDIATE: (1) run `@requirements_validator` remediation workflow, (2) update `output/generated_docs/extracted_requirements.xlsx`, (3) re-run validation, (4) return to Gate 2 until APPROVED/PROCEED

### Step 8: Test Case Generation
Invoke `@test_case_generator` (uses Claude Opus 4). The agent runs
`scripts/generate_test_cases.py export`, authors the test cases (LLM judgment) to
`output/test_cases/_llm_test_cases.json`, then runs `scripts/generate_test_cases.py build`.
Output: `output/test_cases/generated_test_cases.xlsx`

### Step 9: Test Case Validation (LLM-driven)
Invoke `@test_case_validator` (uses Claude Opus 4). The agent loads the
test-case-quality-check + banking-domain-validator skills, judges each test case with
the LLM, and persists the report via `scripts/llm_validate.py`.
Output: `output/validation/test_case_validation_report.xlsx`, `output/remediation/test_cases_remediation_log.xlsx`

### Step 10: Test Case Remediation
Invoke `@test_case_validator` with the remediation flag (uses Claude Opus 4).
```
@test_case_validator --remediate
```
This step applies automated fixes based on `output/remediation/test_cases_remediation_log.xlsx` and updates `output/test_cases/generated_test_cases.xlsx`.

### Step 11: 🛑 HUMAN REVIEW GATE 3
Present test case results for review:
```
══════════════════════════════════════════════════════════
🛑 HUMAN REVIEW GATE 3: Test Case Review
══════════════════════════════════════════════════════════
File: output/test_cases/generated_test_cases.xlsx
Validation Report: output/validation/test_case_validation_report.xlsx
Quality Gate Status: PASS_RATE = (PASS / total) * 100
COVERAGE: Requirements covered / Total requirements
Action Required: APPROVED | REMEDIATE | REJECT
══════════════════════════════════════════════════════════
```
- If APPROVED: continue to Step 12
- If REMEDIATE: (1) run `@test_case_validator --remediate` again, (2) re-validate, (3) return to Gate 3
- If REJECT: terminate pipeline, write summary with rejection status

### Step 12: Traceability Generation
```powershell
python scripts/generate_traceability.py
```
Output: `output/traceability/traceability_matrix.xlsx`

### Step 13: Final Output Verification
Verify all required files exist:
- `output/generated_docs/extracted_requirements.xlsx`
- `output/validation/requirements_validation_report.xlsx`
- `output/generated_docs/{project_name}_context_complete.md`
- `output/test_cases/generated_test_cases.xlsx`
- `output/validation/test_case_validation_report.xlsx`
- `output/traceability/traceability_matrix.xlsx`

If any file is missing, stop pipeline, report which files are missing, include last successful step, and do not generate final summary as "Complete".

### Step 14: Pipeline Summary
Generate `output/generated_docs/pipeline_execution_summary.md` with status = "Complete" only if all Step 13 files exist.

## Model Configuration
All LLM-based operations use **Claude Opus 4** for maximum quality:
- Context Generation: Claude Opus 4
- Requirements Extraction: Claude Opus 4
- Requirements Validation: Claude Opus 4
- Requirements Remediation: Claude Opus 4
- Test Case Generation: Claude Opus 4
- Test Case Validation: Claude Opus 4
- Test Case Remediation: Claude Opus 4

## Behavior Guidelines
- Always wait for human approval at review gates before proceeding
- Report progress after each step
- Domain is auto-detected from documents

## Error Handling
- If any script exits non-zero, stop workflow and report the error
- If user rejects at any gate, terminate and write summary with rejection status
- If required output files are missing, do not mark pipeline as complete
