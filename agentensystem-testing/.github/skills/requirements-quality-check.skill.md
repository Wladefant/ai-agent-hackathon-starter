---
name: requirements-quality-check
description: Performs deep quality analysis on requirements using INVEST criteria and domain-specific patterns. Identifies issues and suggests improvements.
---

# Requirements Quality Check Skill

## Purpose
Perform comprehensive quality analysis on extracted requirements beyond basic validation.

## When to Invoke
Use this skill when:
- Requirements have high FAIL/SOFT-FAIL rate (>30%)
- Before human review gate for requirements
- After remediation to verify improvements
- When user asks to "improve" or "enhance" requirements

## Quality Dimensions

### 1. INVEST Criteria Analysis
Score each requirement against INVEST:

| Criterion | Question | Weight |
|-----------|----------|--------|
| **I**ndependent | Can this requirement be implemented without other requirements? | 15% |
| **N**egotiable | Is there room for discussion on implementation? | 10% |
| **V**aluable | Does it deliver business value? | 20% |
| **E**stimable | Can effort be estimated? | 15% |
| **S**mall | Is it small enough for one iteration? | 15% |
| **T**estable | Are there clear acceptance criteria? | 25% |

### 2. Ambiguity Detection
Flag requirements containing:
- Subjective terms: "user-friendly", "fast", "efficient", "robust"
- Unbounded terms: "all", "never", "always" without exceptions
- Vague quantities: "some", "few", "many", "most"
- Missing actors: "the system" without specifying which

### 3. Completeness Check
Verify presence of:
- Clear subject (who/what performs the action)
- Specific verb (what action is performed)
- Measurable object (what is affected)
- Conditions (when/under what circumstances)
- Constraints (limits, boundaries)

### 4. Consistency Analysis
Detect:
- Conflicting requirements (same component, different behaviors)
- Duplicate requirements (>80% text similarity)
- Missing dependency declarations
- Circular dependencies

### 5. Traceability Gaps
Identify:
- Requirements without source documents
- Requirements not linked to any standard/regulation
- Orphan requirements (no test coverage)
- Missing upstream/downstream links

## Remediation Suggestions

### For Ambiguous Requirements
```
Original: "System shall be fast"
Improved: "System shall respond within 100ms for 95% of requests under normal load (1000 TPS)"
```

### For Incomplete Requirements
```
Original: "Validate payments"
Improved: "BeJoviIncomingApi shall validate incoming pacs.008 messages against ISO 20022 XSD schema within 50ms, returning validation errors with specific field references"
```

### For Non-Testable Requirements
```
Original: "System shall handle errors gracefully"
Improved: "System shall log all errors with timestamp, correlation ID, and stack trace; return structured error response with error code and user-friendly message; retry transient failures up to 3 times with exponential backoff"
```

## Output Format
Generate a quality report with:
1. Overall quality score (0-100)
2. Score breakdown by INVEST dimension
3. Top 5 issues with severity
4. Specific remediation suggestions
5. Requirements needing manual review
