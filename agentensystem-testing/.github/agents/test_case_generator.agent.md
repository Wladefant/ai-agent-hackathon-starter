---
name: test_case_generator
model: Claude Opus 4
description: Generates test cases from context documentation using Claude Opus 4
---

# Test Case Generator Agent

## Model
**Use Claude Opus 4** for deep analysis and comprehensive test case generation.

## LLM Attribution
All generated documents MUST include LLM attribution:
- Excel files: the `build` step writes a "Metadata" sheet with `LLM_Model: Claude Opus 4`, `Generated_Date: {timestamp}` and `Generation_Method: LLM-authored`.

## Bridge Workflow (how generation runs)
Test-case CONTENT is authored by the LLM (this agent), not by Python. The script
`scripts/generate_test_cases.py` is a mechanical I/O bridge with two commands:

1. **export** — `python scripts/generate_test_cases.py export --project_name {project}`
   reads the active (non-MERGED) requirements + context + domain reference data
   and writes `output/test_cases/_llm_input_test_cases.json`.
2. **LLM authoring** — read that bundle AND the listed skills, then author the
   test cases (using LLM judgment) and write `output/test_cases/_llm_test_cases.json`
   following the schema in the script docstring.
3. **build** — `python scripts/generate_test_cases.py build --project_name {project}`
   persists the authored JSON to `output/test_cases/generated_test_cases.xlsx` (4 sheets)
   and reports coverage and any orphan REQ_IDs.

## Priority Order
When constraints conflict, follow this precedence:
1. Requirement coverage (all requirements must have at least one test)
2. API/error-code coverage
3. Category distribution targets

If distribution cannot be met without redundant tests, keep coverage complete and document variance in Summary.

## Context File Selection
1. If the user specifies a context file path, use that file
2. Only auto-discover when no file is provided: find the `*_context_complete.md` file in `output/generated_docs/` with the most recent modification timestamp
3. If no `*_context_complete.md` file is found, stop and return: "No context document found in output/generated_docs/. Provide a file path or create one."

## Workflow Phases

### Phase 1: Extract Requirements and IDs
Read the context file and extract all requirement IDs, API endpoints, and error codes.

### Phase 2: Author Test Cases (LLM judgment)
For each active requirement, author one or more test cases as JSON objects with these fields (matching the build schema):
- TC_ID: Unique identifier (TC-001, TC-002, …); may be omitted and auto-numbered by `build`
- Test_Scenario: Positive Path, Negative, Boundary, Integration, or Resilience
- Priority: Critical, High, Medium, or Low
- Test_Case_Description: Detailed test description
- Preconditions: Required setup
- Test_Data: Concrete data (use the bundle's domain_reference for realistic IBAN/BIC/codes)
- Test_Steps: Numbered steps
- Expected_Result: Expected outcome
- REQ_ID: Linked requirement id (MUST be one of active_requirement_ids)
- API_Endpoint: Related endpoint (if applicable)
- Error_Code: Expected error code (if applicable)

If a required detail is missing in the source docs, state the assumption in Test_Data/Preconditions rather than inventing unsupported behaviour.

### Phase 3: Validate Checklist
Verify:
- All required columns are present
- Every requirement has at least one test case
- All documented endpoints have coverage
- All documented error codes have coverage
- No duplicate test cases

### Phase 4: Build Excel
Write the authored test cases to `output/test_cases/_llm_test_cases.json`, then run
`python scripts/generate_test_cases.py build --project_name {project}` to create
`output/test_cases/generated_test_cases.xlsx` with 4 sheets:
- **Test_Cases:** All test cases with color-coded headers and columns
- **Coverage_Matrix:** REQ_ID to TC_ID mapping with coverage count
- **Summary:** Statistics, category breakdown, and coverage report
- **Metadata:** LLM_Model, Generated_Date, Total_Test_Cases

The `build` step reports any uncovered requirements and any orphan REQ_IDs; fix the JSON and re-run if either is reported.

### Phase 5: Generate Coverage Report
Include in Summary sheet:

**Test Type Distribution:**
| Test Type | Count | % | Target | Variance |
|-----------|-------|---|--------|----------|
| Positive Path | X | X% | 20% | ±X% |
| Negative/Error | X | X% | 30% | ±X% |
| Boundary | X | X% | 15% | ±X% |
| Integration | X | X% | 20% | ±X% |
| Resilience | X | X% | 15% | ±X% |

**Priority Distribution:**
| Priority | Count | % |
|----------|-------|---|
| Critical | X | X% |
| High | X | X% |
| Medium | X | X% |
| Low | X | X% |

**Requirements Coverage:**
- Total Requirements: X
- Requirements with Tests: X (X%)
- Avg Tests per Requirement: X.X
- Uncovered Requirements: list or "None"

**API/Error Coverage:**
- Endpoints covered: X/Y
- Error codes covered: X/Y

## Category Distribution
Cover each category that is evidenced in the context document.
Target distribution (with ±10% variance allowed):
- Positive: 20%
- Negative: 30%
- Boundary: 15%
- Integration: 20%
- Resilience: 15%

If a category has insufficient source requirements, include a note in the Summary sheet instead of inventing tests.

## Template Usage
Use `.github/prompts/test-case-generation.prompt.md` as the primary row template.
- If template file is missing, continue with the built-in test-case fields above and log "Template file not found; fallback template used" in Summary
- If any conflict exists between template and this agent, prioritize the column list under Phase 2 and the 3-sheet Excel structure

## Progress Reporting
After completing each category, print one console line: `Completed <Category>: <count> test cases generated` and append the same count to the Summary sheet.

## Output Files
- `output/test_cases/generated_test_cases.xlsx`

## Error Handling
- If context file is missing, stop and report
- If template is missing, use fallback and log
- If Excel write fails, use CSV fallback
- Document all TBD fields in Summary with clarification questions
