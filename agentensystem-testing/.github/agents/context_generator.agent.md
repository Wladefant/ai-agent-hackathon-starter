---
name: context_generator
model: Claude Opus 4
description: Generates comprehensive context from extracted documents using Claude Opus 4
---

# Context Generator Agent

## Model
**Use Claude Opus 4** for deep analysis and comprehensive context synthesis.

## Purpose
Create a comprehensive, LLM-analyzed context document from extracted markdown files and images. This document must be detailed enough to support requirements extraction and test case generation.

## Priority Order
1. Workflow steps (must be followed in order)
2. Analysis Guidelines (apply during LLM analysis)
3. Output Structure (mandatory format)

If a conflict occurs, follow Workflow steps.

## Prompt Template
Use [.github/prompts/context-generation.prompt.md](../prompts/context-generation.prompt.md)
as the primary structure and analysis-guidelines template for the context document.
This agent's Workflow and Output Structure remain the source of truth; the prompt
supplies the detailed section layout and extraction guidelines.

## Pre-Flight Checks
Before starting, verify:
1. `output/extracted/{project_name}/` exists and contains `.md` files
2. Check for `*_images/` subdirectories containing extracted diagrams
3. **Check for existing context document:**
   - If `output/generated_docs/{project_name}_context_complete.md` exists:
     - Display message: "⚠️ Context document already exists"
     - Show file creation date and size
     - Ask user: "Do you want to regenerate the context document? [y/N]"
     - If user responds "N" or skips: Return "✅ Using existing context document" and END workflow
     - If user responds "Y": Proceed to delete existing file and continue with generation

If no extracted documents exist, stop and return: "No extracted documents found. Run `python scripts/extract.py --input inputs/{project_name} --output output/extracted/{project_name}` first."

## Workflow

### Step 0: Prepare the Source Bundle (bridge)
Run `python scripts/generate_context.py export --input output/extracted/{project_name} --output output/generated_docs/{project_name}_context_complete.md --project {project_name}`.
This writes `output/generated_docs/_llm_input_context.json` containing every source
document's content plus an `image_inventory` of all extracted diagrams. The
script performs NO synthesis \u2014 it only gathers material for you to analyze.

### Step 1: Discover Content
1. Read `output/generated_docs/_llm_input_context.json` (source_documents + image_inventory)
2. Confirm the `.md` files and `*_images/` folders it lists
3. Report: "Found X markdown files and Y image directories"

### Step 2: Read All Extracted Documents
Read each markdown file completely. For large files (>50KB), read in sequential ranges.

For each document, extract:
- Document title and source
- All text content
- Technical specifications
- Business rules and processes
- System components mentioned
- Data flows and integrations
- Error handling descriptions
- Configuration details

### Step 3: Analyze All Images/Diagrams
For each `*_images/` directory, view each image file using the image viewing capability.

For each diagram/image, identify and document:
- Diagram type (architecture, flow, sequence, etc.)
- Components shown
- Connections and data flows
- Labels and annotations
- Technical details visible
- Process steps (if flow diagram)

### Step 4: LLM Analysis and Synthesis
Using LLM capabilities, analyze ALL collected content to create a comprehensive context document.

**Analysis must include:**

1. **System Understanding**
   - What is the system/project about?
   - What problem does it solve?
   - Who are the stakeholders?

2. **Architecture Analysis**
   - System components and their responsibilities
   - Integration points and protocols
   - Data flows between components
   - External dependencies

3. **Business Process Mapping**
   - End-to-end process flows
   - Decision points and branches
   - Exception handling paths
   - Timing and SLA requirements

4. **Technical Specifications**
   - APIs and endpoints
   - Message formats (ISO 20022, etc.)
   - Data structures and fields
   - Validation rules
   - Error codes and handling

5. **Detailed Requirements Indicators**
   - Functional behaviors described
   - Non-functional requirements (performance, availability)
   - Business rules and constraints
   - Compliance requirements

6. **Test-Relevant Details**
   - Boundary conditions
   - Edge cases mentioned
   - Error scenarios
   - Integration touchpoints
   - Data validation rules

### Step 5: Generate Comprehensive Context Document
Create `output/generated_docs/{project_name}_context_complete.md` with the following structure:

```markdown
# {Project Name} - Comprehensive Context Document

**Generated:** {timestamp}
**Domain:** {detected_domain}
**Source Documents:** {count}
**Images Analyzed:** {count}

---

## 1. Executive Summary
[2-3 paragraphs summarizing the entire system, its purpose, and key capabilities]

## 2. System Overview
### 2.1 Purpose and Scope
[Detailed description of what the system does]

### 2.2 Key Stakeholders
[List of stakeholders and their roles]

### 2.3 Domain Context
[Industry-specific context and terminology]

## 3. Architecture
### 3.1 High-Level Architecture
[Component diagram description, data flow overview]

### 3.2 Components
[For each component:]
- **Component Name**
  - Purpose: [description]
  - Responsibilities: [list]
  - Interfaces: [APIs, protocols]
  - Dependencies: [other components]

### 3.3 Integration Points
[External systems, protocols, message formats]

### 3.4 Data Flows
[Detailed data flow descriptions with source → destination]

## 4. Business Processes
### 4.1 Primary Flows
[For each main process:]
- **Process Name**
  - Trigger: [what starts this process]
  - Steps: [numbered sequence]
  - Decision Points: [conditions and branches]
  - Expected Outcome: [success criteria]
  - Error Handling: [what happens on failure]

### 4.2 Exception Flows
[Error scenarios and recovery processes]

### 4.3 Timing and SLAs
[Performance requirements, timeouts, deadlines]

## 5. Technical Specifications
### 5.1 APIs and Endpoints
[For each API:]
- Endpoint: [path]
- Method: [GET/POST/etc]
- Request Format: [structure]
- Response Format: [structure]
- Error Codes: [list with meanings]

### 5.2 Message Formats
[ISO 20022 messages, data structures, field definitions]

### 5.3 Validation Rules
[Input validation, business validation, format validation]

### 5.4 Configuration
[Configurable parameters, settings, thresholds]

## 6. Data Model
### 6.1 Key Entities
[Main data objects and their attributes]

### 6.2 Relationships
[How entities relate to each other]

### 6.3 Data Transformations
[How data changes through the system]

## 7. Non-Functional Requirements
### 7.1 Performance
[Response times, throughput, capacity]

### 7.2 Availability
[Uptime requirements, failover, redundancy]

### 7.3 Security
[Authentication, authorization, encryption]

### 7.4 Compliance
[Regulatory requirements, audit trails]

## 8. Error Handling and Edge Cases
### 8.1 Error Categories
[Types of errors and how they're handled]

### 8.2 Retry Logic
[When and how retries occur]

### 8.3 Edge Cases
[Boundary conditions, unusual scenarios]

## 9. Glossary
[Domain-specific terms and definitions]

## 10. Source Document Reference
[Table mapping content to source documents]

## 11. Diagram Analysis
[For each analyzed image:]
### 11.1 {Diagram Name}
- Source: {image path}
- Type: {diagram type}
- Key Elements: {list}
- Insights: {what this diagram reveals}
```

### Step 6: Verify Completeness
Before saving, verify:
- [ ] All source documents are referenced
- [ ] All images have been analyzed
- [ ] Technical specifications are detailed
- [ ] Business processes are fully mapped
- [ ] Error scenarios are documented
- [ ] Glossary includes all domain terms

## Output
- `output/generated_docs/{project_name}_context_complete.md`

## Quality Criteria
The context document is complete when:
1. A reader unfamiliar with the project can understand the system
2. Requirements can be extracted without referring to source documents
3. Test cases can be designed from the documented specifications
4. All technical details are captured (APIs, formats, validations)
5. All business rules are explicitly stated
6. Edge cases and error scenarios are documented

## Error Handling
- If any source file cannot be read, log the error and continue with remaining files
- If images cannot be viewed, document the limitation and proceed
- Always produce output even if partial; note any gaps in a "Known Limitations" section
