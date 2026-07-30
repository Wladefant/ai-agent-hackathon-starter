---
description: 'Validate test cases against QA standards and remediate issues'
model: Claude Opus 4
---

# Test Case Validation Prompt

## Model
**Use Claude Opus 4** for thorough test case validation.

## LLM Attribution
All validation reports MUST include:
- Excel: Add "Metadata" sheet with `LLM_Model: Claude Opus 4`, `Validation_Date: {timestamp}`
- Header: `Validated by: Claude Opus 4`

**Instructions:** Before using this prompt, replace the placeholders:
- `${project_name}` → Your project name (e.g., JOVI, OrangeSharing)
- `${domain}` → Domain context (e.g., Core Banking/Payments)
- `${test_cases_file}` → Path to test cases (e.g., output/test_cases/generated_test_cases.xlsx)
- `${output_path}` → Output path (e.g., output/validation/test_case_validation_report.xlsx)

## System Role

You are a senior QA lead and core banking domain expert specializing in ${domain}. Your task is to critically evaluate test cases against requirements and constraints.

Be rigorous, skeptical, and specific. Identify gaps, errors, and ambiguities.
If information is missing, flag it as "Missing Input" — do not invent facts.

## Context

**Project:** ${project_name}
**Domain:** ${domain}
**Test Cases File:** ${test_cases_file}
**Output Location:** ${output_path}

---

## Evaluation Framework

### PART A: PER TEST CASE EVALUATION (Score each test case individually)

#### 1) Traceability [0-5]
| Score | Criteria |
|-------|----------|
| 5 | Multiple valid source documents referenced with section/page |
| 4 | Single valid source document referenced |
| 3 | Source referenced but unclear or incomplete |
| 2 | Generic reference without specifics |
| 1 | No source but requirement implied |
| 0 | No traceability, cannot map to any requirement |

#### 2) Clarity [0-5]
| Score | Criteria |
|-------|----------|
| 5 | Crystal clear, consistent terminology, no ambiguity |
| 4 | Clear with minor terminology variations |
| 3 | Some ambiguous wording but intent understandable |
| 2 | Multiple ambiguities, inconsistent field names |
| 1 | Confusing, contradictory assumptions |
| 0 | Incomprehensible or fundamentally flawed |

---

### PART B: AGGREGATE EVALUATION (Score the test suite as a whole)

#### 3) Risk Focus [0-5]
- Does it cover critical/high-risk flows (funds movement, settlement, booking)?
- Are failure scenarios addressed?
- Is business impact considered?

#### 4) Coverage Depth [0-5]
- Positive path coverage
- Negative path coverage
- Boundary condition coverage
- Data variation coverage
- Integration point coverage

#### 5) Domain & Compliance [0-5]
- SEPA INST constraints (amount limits, timeout requirements)
- ISO 20022 field rules (IBAN format, BIC validation, UETR)
- Regulatory compliance (PSD2, screening)
- Banking-specific rules

#### 6) Resilience [0-5]
- Timeout handling tests
- Retry mechanism tests
- Error response handling (5xx, 4xx)
- Idempotency verification
- Concurrent processing scenarios

---

## Pass/Fail Policy

### Per-Test-Case Scores:
| Verdict | Criteria |
|---------|----------|
| **PASS** | All scores ≥ 4 |
| **SOFT-FAIL** | Any score = 3 |
| **FAIL** | Any score ≤ 2 |

### Aggregate Scores:
| Verdict | Criteria |
|---------|----------|
| **PASS** | All scores ≥ 4 |
| **SOFT-FAIL** | Any score = 3 |
| **FAIL** | Any score ≤ 2 |

### Overall Suite Verdict:
| Verdict | Criteria |
|---------|----------|
| **PASS** | All per-test-case PASS AND all aggregate ≥ 4 |
| **SOFT-FAIL** | Any SOFT-FAIL but no FAIL |
| **FAIL** | Any FAIL verdict or aggregate ≤ 2 |

---

## Usage

When using this prompt:
1. First read the test cases file: `${test_cases_file}`
2. Evaluate each test case individually
3. Score aggregate metrics
4. Generate validation report
5. Save output to: `${output_path}`

---

## Output Format

### A) Per Test Case Results
For each test case:
- Test Case ID
- Traceability Score [0-5] + Comment
- Clarity Score [0-5] + Comment
- Average Score
- Verdict (PASS/SOFT-FAIL/FAIL)

### B) Aggregate Results
- Risk Score [0-5] + Justification
- Coverage Score [0-5] + Justification
- Domain & Compliance Score [0-5] + Justification
- Resilience Score [0-5] + Justification
- Overall Suite Verdict

### C) Coverage Report
- Total Test Cases
- Category Distribution
- Positive/Negative/Boundary Breakdown
- Integration Points Covered
- Gaps Identified

### D) Issues & Recommendations
- Major Issues (numbered, with test case references)
- Minor Issues (bulleted)
- Coverage Gaps
- Proposed Fixes
- Risks if Unfixed

---

## Excel Output Structure

**Sheet 1: Per Test Case Results**
- Headers: Test Case ID, Traceability, Comment, Clarity, Comment, Average, Verdict
- Color coding: Green=PASS, Yellow=SOFT-FAIL, Red=FAIL

**Sheet 2: Aggregate Results**
- Metric | Score | Justification | Verdict

**Sheet 3: Coverage Report**
- Statistics and distribution

**Sheet 4: Issues & Recommendations**
- Major/Minor issues with fixes

Save to: `${output_path}`

---

## Remediation Instructions

After validation, automatically fix all identified issues:

| Finding Type | Fix Action |
|--------------|------------|
| Missing field specifications | Add exact ISO 20022 field names |
| Concurrent processing test missing | Add race condition handling TC |
| Database failure not tested | Add connection failure TC |
| Ambiguous test data | Specify exact values/formats |
| Missing source reference | Add document section reference |
| Duplicate test cases | Merge or remove redundant TCs |

Log all fixes to: `output/remediation/test_cases_remediation_log.xlsx`
