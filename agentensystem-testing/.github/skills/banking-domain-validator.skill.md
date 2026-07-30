---
name: banking-domain-validator
description: Validates requirements and test cases against Core Banking/Payments domain standards including ISO 20022, SEPA, and payment processing best practices.
---

# Banking Domain Validator Skill

## Purpose
Apply domain-specific validation rules for Core Banking/Payments requirements and test cases.

## When to Invoke
Use this skill when:
- Validating requirements for payment systems
- Checking ISO 20022 compliance (pacs.008, pacs.002, camt messages)
- Verifying SEPA Instant Payment rules
- Validating error codes and handling

## Domain Validation Rules

### ISO 20022 Message Compliance
Check that requirements mentioning ISO 20022 include:
- Specific message type (pacs.008, pacs.002, camt.056, etc.)
- Required fields for the message type
- XSD validation references
- Error handling for invalid messages

### SEPA Instant Payment Rules
Verify compliance with:
- 10-second end-to-end processing requirement
- €100,000 transaction limit
- 24/7/365 availability
- Irrevocable payment processing
- Reason codes for rejections (FF01, AM23, AB08, etc.)

### Payment Status Codes
Ensure test cases cover all relevant status transitions:
| Code | Status | Required Coverage |
|------|--------|-------------------|
| 00 | Created | Positive path |
| 01 | Acknowledged | Positive path |
| 05 | Sent to Screening | Integration |
| 06 | Timeout | Resilience |
| 90 | Rejected | Negative |
| 91 | Technical rejection | Negative |

### IBAN/BIC Validation
Requirements involving account validation should specify:
- IBAN format validation (ISO 13616)
- BIC lookup and verification
- Account existence check
- Closed account handling

## Validation Checklist

### Requirements Validation
- [ ] Uses domain-specific terminology correctly
- [ ] References applicable standards (ISO 20022, SEPA rulebook)
- [ ] Includes specific message types where applicable
- [ ] Defines measurable SLAs (response time, availability)
- [ ] Specifies error codes and handling

### Test Case Validation
- [ ] Covers positive and negative paths for payment flows
- [ ] Includes boundary tests for amount limits
- [ ] Tests timeout and retry scenarios
- [ ] Validates all relevant status code transitions
- [ ] Includes integration tests with external systems (TIPS, RT1, STET)

## Output
When invoked, produce a domain compliance report with:
1. Compliance score (0-100%)
2. Missing domain-specific requirements
3. Uncovered error scenarios
4. Recommendations for improvement
