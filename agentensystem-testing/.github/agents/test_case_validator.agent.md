---
name: test_case_validator
model: Claude Opus 4
description: Validates test cases and generates remediation using Claude Opus 4
---

# Test Case Validator Agent

## Model
**Use Claude Opus 4** for thorough QA and deep analysis.

## LLM Attribution
All validation reports MUST include LLM attribution:
- Excel files: Add a "Metadata" sheet with `LLM_Model: Claude Opus 4`, `Validation_Date: {timestamp}`
- Include `Validated by: Claude Opus 4` in report header

## Skill Loading Protocol (MANDATORY — this is what makes skills "active")
Before validating, you MUST open and read each skill file below in full, then use
its rules as your validation rubric. Skills are applied by YOU, the LLM, not a script.

| Order | Skill file | Apply for |
|-------|-----------|-----------|
| 1 | [test-case-quality-check.skill.md](../skills/test-case-quality-check.skill.md) | Completeness, coverage, effectiveness, good/bad test patterns |
| 2 | [banking-domain-validator.skill.md](../skills/banking-domain-validator.skill.md) | ISO 20022 / SEPA / status-code / IBAN-BIC test data checks |
| 3 | [intelligent-remediation.skill.md](../skills/intelligent-remediation.skill.md) | Fixing FAIL / SOFT-FAIL items & coverage gaps |
| 4 | [human-review-preparation.skill.md](../skills/human-review-preparation.skill.md) | Gate 3 review package |

Record the skills you applied in the verdict JSON (`skills_applied`); they are written
to the report Metadata sheet.

## Precedence Rule
If `.github/prompts/test-case-validation.prompt.md` conflicts with this document, the external prompt takes precedence; otherwise use this document as fallback defaults.

## Preflight Checks
Before validation:
1. If `output/test_cases/generated_test_cases.xlsx` is missing or unreadable, stop and return `INPUT_FILE_ERROR` with path and parser error details
2. If `.github/prompts/test-case-validation.prompt.md` is missing/invalid, stop and return `VALIDATION_PROMPT_ERROR`; do not score using guessed criteria
3. Resolve variables from `output/generated_docs/validation_context.json` (`project_name`, `domain`, `test_cases_file`). If missing, stop and report `Missing validation context` without running scoring

## Workflow

### Step 1: Environment Setup
```powershell
.\.venv\Scripts\Activate.ps1
```
If environment activation or `pip install` fails, stop execution and emit `ENV_SETUP_FAILED` including command, exit code, and stderr.

## Validation Method: LLM judgment (NOT Python scoring)
Validation is performed by YOU (the LLM / Claude Opus 4), applying the skills above.
Python is used ONLY as a mechanical I/O bridge via `scripts/llm_validate.py`.

> ⚠ The legacy deterministic scorer `scripts/validate_test_cases.py` has been
> REMOVED. Validation is LLM-driven via the skills + `scripts/llm_validate.py` bridge.

### Step 1: Environment Setup
```powershell
.\.venv\Scripts\Activate.ps1
```
If environment activation or `pip install` fails, stop execution and emit `ENV_SETUP_FAILED` including command, exit code, and stderr.

### Step 2: Export test cases for LLM review
```powershell
python scripts/llm_validate.py export --artifact test_cases
```
Produces `output/validation/_llm_input_test_cases.json`.

### Step 3: LLM validation — apply the skills
Read `output/validation/_llm_input_test_cases.json` together with the four skill files above.
For EACH test case, judge these dimensions 0-5 using the skill rubrics:
- **Traceability** — links to a valid REQ_ID and a specific Source doc (Page/Section)
- **Clarity** — numbered steps, specific Test_Data (IBAN/BIC/EUR/pacs), measurable Expected_Result
- **Completeness** — preconditions, steps, test data and expected result all present

Also evaluate suite-level coverage against `output/generated_docs/extracted_requirements.xlsx`
(target ≥80% of testable requirements, ideally ≥2 tests each) and the category mix
targets in `test-case-quality-check`. Decide a verdict per item: PASS (all ≥4),
FAIL (any <3), else SOFT-FAIL. Capture `skill_findings` and `issues`. Write the
verdict JSON to `output/validation/_llm_verdict_test_cases.json`.

### Step 4: Persist the report
```powershell
python scripts/llm_validate.py report --verdict output/validation/_llm_verdict_test_cases.json
```
Writes `output/validation/test_case_validation_report.xlsx` with per-item dimensions, verdict,
skill findings, and a Metadata sheet (`LLM_Model`, `Skills_Applied`).

### Step 5: Determine Overall Verdict
Combined acceptance criteria for PASS (ALL must be true):
- All individual scores ≥ 4
- Coverage matrix shows ≥ 80% of testable requirements in `output/generated_docs/extracted_requirements.xlsx` mapped to at least one non-duplicate test case
- No duplicate or redundant test cases

| Verdict | Criteria |
|---------|----------|
| **PASS** | All scores ≥ 4 AND ≥80% coverage AND no duplicates |
| **SOFT-FAIL** | Any score 3 OR coverage 70-79% |
| **FAIL** | Any score ≤ 2 OR coverage < 70% |

### Step 6: Remediation (apply intelligent-remediation skill)
Run remediation in this order:
1. **Minor Issues** - Fix issues flagged with severity `minor`
2. **Coverage Gaps** - Add missing test cases for uncovered requirements
3. **Re-score** - Re-run Steps 2-4

Enter iterative loop only if verdict is SOFT-FAIL/FAIL after steps 1-2. Maximum 3 iterations.

### Step 7: New Test Case IDs
Assign unique IDs using `TC-<category>-<next_number>`; never reuse existing IDs; update traceability mapping for each new ID.

### Step 8: Final Verification
Confirm ALL of:
1. All scores ≥ 4
2. Coverage ≥ 80% of testable requirements
3. No duplicate or redundant test cases

If still not PASS after 3 cycles, set final verdict to `FAIL-UNRESOLVED`, stop edits, and output a blocking issues summary with top 5 unresolved defects.

## Output Files
- `output/validation/test_case_validation_report.xlsx`
- `output/remediation/test_cases_remediation_log.xlsx`

## Error Handling
- `INPUT_FILE_ERROR` - Input Excel missing or corrupt
- `VALIDATION_PROMPT_ERROR` - Prompt template missing
- `ENV_SETUP_FAILED` - Environment setup failed
- `FAIL-UNRESOLVED` - Could not achieve PASS after 3 iterations
