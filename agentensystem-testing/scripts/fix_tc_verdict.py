#!/usr/bin/env python3
"""Fix script to enrich test case verdict JSON with TC_IDs."""
import json

# Read test cases to get TC_IDs
with open('output/test_cases/_llm_test_cases.json', 'r', encoding='utf-8') as f:
    tc_data = json.load(f)

# Build lookup by title/scenario
tc_map = {}
for tc in tc_data.get('test_cases', []):
    tc_id = tc.get('TC_ID', '')
    title = tc.get('Test_Scenario', '')
    if tc_id and title:
        tc_map[title] = tc_id

print(f'Loaded {len(tc_map)} test case IDs')

# Read verdict
with open('output/validation/_llm_verdict_test_cases.json', 'r', encoding='utf-8') as f:
    verdict = json.load(f)

# Enrich items with TC_IDs
enriched = 0
for item in verdict.get('items', []):
    title = item.get('title', '')
    if title in tc_map:
        item['id'] = tc_map[title]
        enriched += 1
    elif not item.get('id'):
        # Fallback: assign sequential ID if no match
        enriched += 1
        item['id'] = f'TC-JOVI-{enriched:03d}'

# Write enriched verdict
with open('output/validation/_llm_verdict_test_cases.json', 'w', encoding='utf-8') as f:
    json.dump(verdict, f, indent=2, ensure_ascii=False)

print(f'Enriched {enriched} verdict items with TC_IDs')
