---
name: human-review-preparation
description: Prepares comprehensive review materials for human review gates, summarizing key findings and highlighting items requiring attention.
---

# Human Review Preparation Skill

## Purpose
Generate clear, actionable review materials for human approval gates to facilitate faster, more informed decisions.

## When to Invoke
Use this skill:
- Before presenting HUMAN REVIEW GATE 1 (Requirements)
- Before presenting HUMAN REVIEW GATE 2 (Requirements Validation)
- Before presenting HUMAN REVIEW GATE 3 (Test Cases)

## Review Package Structure

### Requirements Review (Gate 1)

Generate a review summary with:

```markdown
# Requirements Review Package

## Quick Stats
| Metric | Value |
|--------|-------|
| Total Requirements | X |
| By Type | FUNC: X, NFR: X, INT: X, COMP: X, DATA: X |
| By Priority | CRITICAL: X, HIGH: X, MEDIUM: X, LOW: X |
| Source Documents | X files referenced |

## Quality Indicators
- Average description length: X words
- Requirements with acceptance criteria: X% 
- Requirements with clear components: X%
- Requirements with traceability: X%

## Items Requiring Attention
[List top 5 requirements that may need manual review]
1. REQ-XXX: [reason for attention]
2. ...

## Coverage Analysis
[Show which document sections generated requirements]

## Recommendation
[ ] APPROVE - Quality meets standards
[ ] NEEDS REVIEW - X items require attention
[ ] REJECT - Significant issues found
```

### Validation Review (Gate 2)

Generate a validation summary with:

```markdown
# Validation Review Package

## Validation Results
| Verdict | Count | Percentage |
|---------|-------|------------|
| PASS | X | X% |
| SOFT-FAIL | X | X% |
| FAIL | X | X% |

## Issue Breakdown
| Issue Type | Count | Severity |
|------------|-------|----------|
| Duplicates | X | High |
| Ambiguous terms | X | Medium |
| Missing traceability | X | Medium |
| Artifacts in text | X | Low |

## Failed Requirements
[List all FAIL requirements with brief reason]

## Soft-Fail Requirements
[List all SOFT-FAIL requirements - may proceed with caution]

## Remediation Potential
- Auto-fixable issues: X (X%)
- Manual review needed: X (X%)
- Cannot be fixed automatically: X (X%)

## Recommendation
[ ] APPROVED - Pass rate acceptable (>80%)
[ ] PROCEED - Acceptable with known issues
[ ] REMEDIATE - Run automated fixes first
```

### Test Case Review (Gate 3)

Generate a test case summary with:

```markdown
# Test Case Review Package

## Quick Stats
| Metric | Value |
|--------|-------|
| Total Test Cases | X |
| By Category | Positive: X, Negative: X, Boundary: X, Integration: X, Resilience: X |
| By Priority | Critical: X, High: X, Medium: X, Low: X |

## Coverage Analysis
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Requirements covered | X/Y | 100% | ✅/⚠️/❌ |
| Avg tests per requirement | X.X | ≥2 | ✅/⚠️/❌ |
| API endpoints covered | X/Y | 100% | ✅/⚠️/❌ |
| Error codes covered | X/Y | 100% | ✅/⚠️/❌ |

## Category Distribution
| Category | Actual | Target | Variance |
|----------|--------|--------|----------|
| Positive | X% | 20% | ±X% |
| Negative | X% | 30% | ±X% |
| Boundary | X% | 15% | ±X% |
| Integration | X% | 20% | ±X% |
| Resilience | X% | 15% | ±X% |

## Validation Results
| Dimension | Avg Score | Min Score |
|-----------|-----------|-----------|
| Completeness | X.X | X |
| Clarity | X.X | X |
| Testability | X.X | X |
| Traceability | X.X | X |

## Items Requiring Attention
[List test cases with scores < 4]

## Uncovered Requirements
[List requirements without test coverage]

## Recommendation
[ ] APPROVED - Coverage and quality acceptable
[ ] REMEDIATE - Add missing tests or fix quality issues
[ ] REJECT - Significant gaps in coverage
```

## Decision Support

### Approval Criteria by Gate

| Gate | Auto-Approve If | Manual Review If | Reject If |
|------|-----------------|------------------|-----------|
| Gate 1 | All requirements have ID, Title, Description | Any "TBD" fields | <10 requirements extracted |
| Gate 2 | Pass rate ≥80% | Pass rate 60-80% | Pass rate <60% |
| Gate 3 | Coverage ≥80%, all scores ≥4 | Coverage 70-80% | Coverage <70% |

### Common Reviewer Questions

**Gate 1:**
- Are all source documents represented?
- Are requirements at the right granularity?
- Any obvious missing requirements?

**Gate 2:**
- Are failed requirements critical?
- Can auto-remediation fix the issues?
- Are soft-fails acceptable for this project?

**Gate 3:**
- Is coverage sufficient for project risk level?
- Are critical paths well tested?
- Any obvious missing test scenarios?
