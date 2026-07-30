---
name: test-case-quality-check
description: Analyzes test case quality for completeness, coverage, and effectiveness. Identifies gaps and suggests improvements.
---

# Test Case Quality Check Skill

## Purpose
Perform comprehensive quality analysis on generated test cases to ensure effective testing coverage.

## When to Invoke
Use this skill when:
- Test case validation shows issues
- Before human review gate for test cases
- Coverage is below 80%
- User asks to "improve" or "enhance" test cases

## Quality Dimensions

### 1. Test Case Completeness
Each test case must have:
- [ ] Unique TC_ID following naming convention
- [ ] Descriptive title (not just requirement title)
- [ ] Clear preconditions
- [ ] Numbered, actionable test steps
- [ ] Specific expected results with verification criteria
- [ ] Linked requirement ID
- [ ] Appropriate priority assignment

### 2. Coverage Analysis

#### Requirement Coverage
| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Requirements with tests | 100% | Generate missing tests |
| Avg tests per requirement | ≥2 | Add negative/boundary tests |
| Critical requirements coverage | 100% | Prioritize immediately |

#### Test Type Distribution
| Type | Target | Purpose |
|------|--------|---------|
| Positive Path | 20% | Happy path validation |
| Negative/Error | 30% | Error handling, invalid inputs |
| Boundary | 15% | Edge cases, limits |
| Integration | 20% | Component interaction |
| Resilience | 15% | Failure recovery, timeouts |

#### API Endpoint Coverage
- All documented endpoints must have at least 1 positive and 1 negative test
- Error codes must have explicit test coverage

### 3. Test Effectiveness

#### Good Test Patterns
✅ Specific assertions: "Response status code equals 200"
✅ Data verification: "IBAN field matches input value"
✅ Timing validation: "Response received within 10 seconds"
✅ State verification: "Payment status updated to '21' in database"

#### Bad Test Patterns
❌ Vague assertions: "System works correctly"
❌ Missing verification: Steps without expected results
❌ Untestable: "User is satisfied with response"
❌ Duplicate coverage: Multiple tests checking same scenario

### 4. Traceability Check
- Every test links to valid requirement ID
- No orphan tests (tests without requirements)
- Bidirectional traceability verified

## Gap Analysis

### Identify Missing Tests For:
1. **Error Scenarios**
   - Invalid input formats
   - Missing required fields
   - Authentication failures
   - Authorization violations

2. **Boundary Conditions**
   - Minimum/maximum values
   - Empty inputs
   - Very large inputs
   - Special characters

3. **Integration Points**
   - External system timeouts
   - Connection failures
   - Invalid responses from dependencies

4. **Resilience**
   - Retry mechanisms
   - Failover scenarios
   - Recovery after outage

## Output Format
Generate a quality report with:
1. Overall test suite quality score (0-100)
2. Coverage metrics table
3. Distribution analysis vs targets
4. Top 5 gaps with severity
5. Specific test case suggestions for gaps
6. Tests recommended for removal (duplicates)
