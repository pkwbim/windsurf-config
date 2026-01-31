# Skill Creation Deep Dive

## Progressive Disclosure Patterns

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Cascade

### Pattern 1: High-Level Guide with References

Keep SKILL.md as a navigation hub:

```markdown
# PDF Processing

## Quick Start
Extract text with pdfplumber:
[code example]

## Advanced Features
- **Form filling**: See [FORMS.md](references/FORMS.md)
- **API reference**: See [REFERENCE.md](references/REFERENCE.md)
- **Examples**: See [EXAMPLES.md](references/EXAMPLES.md)
```

Cascade loads reference files only when needed.

### Pattern 2: Domain-Specific Organization

For skills with multiple domains:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

When user asks about sales metrics, Cascade only reads `sales.md`.

### Pattern 3: Framework Variants

For skills supporting multiple frameworks:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

When user chooses AWS, Cascade only reads `aws.md`.

## Resource Organization

### Scripts Directory

**Purpose**: Executable code for deterministic operations

**When to include**:
- Code is repeatedly rewritten
- Deterministic reliability needed
- Complex operations benefit from pre-tested code

**Examples**:
- `scripts/rotate_pdf.py` - PDF rotation
- `scripts/convert_format.py` - File conversion
- `scripts/api_client.py` - API interaction

**Benefits**:
- Token efficient
- Deterministic execution
- May execute without loading into context

### References Directory

**Purpose**: Documentation loaded into context as needed

**When to include**:
- API documentation
- Database schemas
- Domain knowledge
- Company policies
- Detailed workflow guides

**Examples**:
- `references/api_docs.md` - API specifications
- `references/schema.md` - Database schema
- `references/policies.md` - Company policies

**Best practices**:
- Keep files focused (one domain per file)
- Include table of contents for files >100 lines
- Use grep-friendly patterns for large files
- Avoid duplication with SKILL.md

### Assets Directory

**Purpose**: Files used in output (not loaded into context)

**When to include**:
- Templates to be copied/modified
- Images, icons, fonts
- Boilerplate code
- Sample documents

**Examples**:
- `assets/logo.png` - Brand assets
- `assets/template.pptx` - PowerPoint template
- `assets/frontend-template/` - HTML/React boilerplate
- `assets/font.ttf` - Typography

**Benefits**:
- Separates output resources from documentation
- Enables file use without context loading

## Writing Effective Descriptions

The description field is the primary trigger mechanism. Include:

1. **What the skill does**
2. **When to use it** (specific triggers)
3. **File types or contexts**

### Good Example
```yaml
description: Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Cascade needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks
```

### Bad Example
```yaml
description: Helps with documents
```

## Skill Structure Patterns

### 1. Workflow-Based (Sequential Processes)

Best for: Clear step-by-step procedures

```markdown
## Overview
Brief introduction

## Workflow Decision Tree
Help user choose the right path

## Step 1: Initial Setup
Instructions

## Step 2: Main Process
Instructions

## Step 3: Finalization
Instructions
```

**Example**: DOCX skill with Reading → Creating → Editing flow

### 2. Task-Based (Tool Collections)

Best for: Different operations/capabilities

```markdown
## Overview
Brief introduction

## Quick Start
Getting started guide

## Task Category 1
Instructions for task type 1

## Task Category 2
Instructions for task type 2
```

**Example**: PDF skill with Merge → Split → Extract operations

### 3. Reference/Guidelines (Standards)

Best for: Brand guidelines, coding standards

```markdown
## Overview
Brief introduction

## Guidelines
Core principles

## Specifications
Detailed specs

## Usage Examples
Concrete examples
```

**Example**: Brand styling with Colors → Typography → Features

### 4. Capabilities-Based (Integrated Systems)

Best for: Multiple interrelated features

```markdown
## Overview
Brief introduction

## Core Capabilities

### 1. Feature One
Description and usage

### 2. Feature Two
Description and usage

### 3. Feature Three
Description and usage
```

**Example**: Product Management with numbered capability list

## Common Pitfalls

### 1. Over-Explaining
**Problem**: Assuming Cascade doesn't know common concepts
**Solution**: Only add context Cascade doesn't have

### 2. Monolithic SKILL.md
**Problem**: Putting everything in one file
**Solution**: Split into references when approaching 500 lines

### 3. Vague Descriptions
**Problem**: Generic descriptions that don't trigger properly
**Solution**: Include specific scenarios and file types

### 4. Missing References
**Problem**: Not linking to supporting files
**Solution**: Clearly reference scripts/references/assets in SKILL.md

### 5. Deeply Nested References
**Problem**: References linking to other references
**Solution**: Keep references one level deep from SKILL.md

## Testing Your Skill

1. **Test with real tasks**: Use the skill on actual work
2. **Notice struggles**: Identify where Cascade gets confused
3. **Check triggering**: Verify automatic invocation works
4. **Validate resources**: Ensure scripts run, references load correctly
5. **Iterate**: Update based on real usage patterns

## Skill Naming Conventions

- Use hyphen-case: `my-skill-name`
- Lowercase letters, digits, hyphens only
- Max 40 characters
- Descriptive and specific
- Match directory name exactly

**Good names**:
- `deploy-to-staging`
- `code-review`
- `setup-dev-environment`

**Bad names**:
- `deploy1`
- `helper`
- `utils`
