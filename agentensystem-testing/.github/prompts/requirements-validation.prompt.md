---
description: 'Validate extracted requirements against quality standards'
model: Claude Opus 4
---

# Requirements Validation Prompt

## Model
**Use Claude Opus 4** for deep validation analysis.

## LLM Attribution
All validation reports MUST include:
- Excel: Add "Metadata" sheet with `LLM_Model: Claude Opus 4`, `Validation_Date: {timestamp}`
- Header: `Validated by: Claude Opus 4`

## Context
You are validating requirements extracted for **${project_name}** in the **${domain}** domain.

## Input
- **Requirements File:** `output/generated_docs/extracted_requirements.xlsx`
- **Context File:** `output/generated_docs/${project_name}_context_complete.md` (if available)

## Validation Framework

### Dimension 1: Completeness [0-5]
Evaluate if all required fields are populated with meaningful content.

| Score | Criteria |
|-------|----------|
| 5 | All fields populated: ID, Title, Description, Type, Priority, Source, Components, Traceability |
| 4 | Missing 1 optional field (Components or Traceability) |
| 3 | Missing 2 fields but core requirement is clear |
| 2 | Multiple fields empty, requirement underspecified |
| 1 | Only ID and Title present |
| 0 | Insufficient information to understand requirement |

### Dimension 2: Clarity [0-5]
Evaluate if the requirement is clear and unambiguous.

| Score | Criteria |
|-------|----------|
| 5 | Crystal clear, single interpretation possible, uses precise language |
| 4 | Clear with minor terminology that could be clarified |
| 3 | Understandable but contains some ambiguous terms |
| 2 | Contains vague terms like "fast", "user-friendly", "efficient" |
| 1 | Multiple interpretations possible, confusing structure |
| 0 | Cannot determine what the requirement means |

**Red Flag Terms:**
- Ambiguous: "fast", "quick", "efficient", "user-friendly", "intuitive", "robust"
- Vague: "some", "few", "many", "most", "etc.", "and so on"
- Unbounded: "all", "never", "always" (without exception handling)

### Dimension 3: Testability [0-5]
Evaluate if the requirement can be verified through testing.

| Score | Criteria |
|-------|----------|
| 5 | Clear Given/When/Then format OR measurable criteria with specific values |
| 4 | Testable with minor clarification (missing specific threshold) |
| 3 | Partially testable, would need assumptions |
| 2 | Difficult to verify, no clear pass/fail criteria |
| 0 | Completely untestable |

**Testable Examples:**
- "System shall respond within 10 seconds" ✓
- "System shall validate IBAN per ISO 13616" ✓
- "System shall be fast" ✗
- "System shall handle errors gracefully" ✗

### Dimension 4: Traceability [0-5]
Evaluate if the requirement can be traced to source and standards.

| Score | Criteria |
|-------|----------|
| 5 | Clear source document, page/section, AND linked to standard/regulation |
| 4 | Source document identified, standard mentioned |
| 3 | Source document identified but no standard linkage |
| 2 | Vague source reference (e.g., "from architecture docs") |
| 1 | No source but inferred from domain knowledge |
| 0 | Cannot trace to any source |

## Verdict Calculation

Verdicts use a **per-dimension** rule (NOT an average), matching the pipeline bridge
(`scripts/llm_validate.py` `derive_verdict`) and `config.json`
(`min_score_pass = 4`, `min_score_soft_fail = 3`):

```
PASS:      every dimension >= 4
FAIL:      any dimension < 3
SOFT-FAIL: otherwise (all dimensions >= 3, but at least one dimension == 3)
```

Worked example: scores [5, 5, 5, 2] -> FAIL (one dimension < 3), even though the
average is 4.25. A single weak dimension cannot be averaged away.

## Validation Output

For each requirement, output:

| Field | Description |
|-------|-------------|
| REQ_ID | Original requirement ID |
| Completeness_Score | 0-5 |
| Clarity_Score | 0-5 |
| Testability_Score | 0-5 |
| Traceability_Score | 0-5 |
| Average_Score | Calculated average |
| Verdict | PASS / SOFT-FAIL / FAIL |
| Issues | List of specific issues found |
| Remediation | Suggested fixes |

## Remediation Guidelines

### For Completeness Issues:
- Missing Components: "Add system components: [suggest based on description]"
- Missing Traceability: "Add reference to: [suggest standard/regulation]"
- Missing Acceptance Criteria: "Add: Given [X], When [Y], Then [Z]"

### For Clarity Issues:
- Ambiguous terms: "Replace '[term]' with specific value: [suggestion]"
- Multiple interpretations: "Split into atomic requirements or clarify scope"
- Vague language: "Quantify '[term]' with measurable criteria"

### For Testability Issues:
- No criteria: "Add acceptance criteria: Given/When/Then format"
- Unmeasurable: "Add threshold: [suggest specific value based on domain]"
- Partial: "Complete acceptance criteria with expected outcome"

### For Traceability Issues:
- No source: "Add source reference from: [suggest likely document]"
- No standard: "Link to: ISO 20022 / SEPA rulebook / [relevant standard]"

## Aggregate Metrics

Calculate and report:

| Metric | Calculation |
|--------|-------------|
| PASS Rate | (PASS count / Total) × 100% |
| Average Completeness | Mean of all Completeness scores |
| Average Clarity | Mean of all Clarity scores |
| Average Testability | Mean of all Testability scores |
| Average Traceability | Mean of all Traceability scores |
| Critical Failures | Count of FAIL verdicts on CRITICAL priority |

## Quality Gate

| Condition | Action |
|-----------|--------|
| PASS Rate >= 80% AND Critical Failures = 0 | Pipeline can proceed |
| PASS Rate >= 60% AND Critical Failures = 0 | Proceed with warnings |
| PASS Rate < 60% OR Critical Failures > 0 | Block pipeline, require remediation |

## Output Files

The bridge `scripts/llm_validate.py report` persists your verdict JSON to:

1. **output/validation/requirements_validation_report.xlsx** — per-requirement
   dimension scores, verdict, issues, and skill findings, plus a Metadata sheet
   (`LLM_Model`, `Skills_Applied`).

Remediation (only when invoked) is applied by `scripts/llm_validate.py remediate`
and logged to:

2. **output/remediation/requirements_remediation_log.xlsx** — the change log for
   each SOFT-FAIL / FAIL requirement that was patched (with backup
   `extracted_requirements.pre_remediation.xlsx`).

## Output Path
Save to: `${output_path}` (default: `output/validation/requirements_validation_report.xlsx`)
