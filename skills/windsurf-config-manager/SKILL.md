---
name: windsurf-config-manager
description: |
  Comprehensive guide for creating, modifying, and managing Windsurf configuration files.
  
  **TRIGGER THIS SKILL WHEN:**
  - User asks about Rules vs Skills vs Workflows vs AGENTS.md
  - User wants to create or modify .windsurf/skills/, .windsurf/rules/, .windsurf/workflows/
  - User asks "where should I put this rule/config?"
  - User asks about trigger modes (always_on, model_decision, glob, manual)
  - User wants to set coding standards, file size limits, or behavioral guidelines
  - User asks which configuration type to use for their needs
  - User mentions: Rule, Skill, Workflow, AGENTS.md, trigger, glob pattern
  - **User asks to CREATE a new workflow** (e.g., "請做一個 workflow", "create a workflow")
  - **User asks to CREATE a new rule** (e.g., "建立一個 rule", "add a rule")
  - **User asks to CREATE a new skill** (e.g., "新增一個 skill")
  
  **DO NOT USE FOR:** General coding questions unrelated to Windsurf configuration.
---

# Windsurf Configuration Manager

This skill helps you create and manage all types of Windsurf configuration files: Skills, Rules, Workflows, and AGENTS.md.

## Quick Decision Guide

**Choose the right configuration type:**

| Need | Use | Location |
|------|-----|----------|
| Complex multi-step task with resources | **Skill** | `.windsurf/skills/<name>/` |
| Behavioral guidelines & preferences | **Rule** | `.windsurf/rules/<name>.md` |
| Repeatable command sequence | **Workflow** | `.windsurf/workflows/<name>.md` |
| Directory-specific instructions | **AGENTS.md** | Any directory |

## 1. Skills

### When to Use Skills
- Complex tasks requiring supporting files (scripts, templates, docs)
- Multi-step workflows with bundled resources
- Domain-specific procedures (deployment, code review, testing)
- Tasks that need reference documentation or executable scripts

### Skill Structure
```
.windsurf/skills/<skill-name>/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
├── scripts/ (optional) - Executable code
├── references/ (optional) - Documentation
└── assets/ (optional) - Templates, images, etc.
```

### Creating a Skill

**Step 1: Initialize**
```bash
# Use the skill-creator's init script if available
python3 /path/to/skill-creator/scripts/init_skill.py <skill-name> --path .windsurf/skills
```

**Step 2: Edit SKILL.md**

Required frontmatter:
```yaml
---
name: skill-name
description: Clear explanation of what the skill does and when to use it. Include specific triggers and contexts.
---
```

**Step 3: Add Resources**
- `scripts/` - Python/Bash scripts for automation
- `references/` - Documentation loaded into context as needed
- `assets/` - Templates, images used in output (not loaded into context)

### Skill Best Practices
- **Concise description**: Include WHAT it does and WHEN to use it
- **Progressive disclosure**: Keep SKILL.md under 500 lines, split into references
- **Clear triggers**: Describe scenarios that should invoke the skill
- **Reference organization**: Use domain-specific files (e.g., `references/aws.md`, `references/gcp.md`)

### Invoking Skills
- **Automatic**: Cascade invokes based on description match
- **Manual**: `@skill-name` in Cascade input

## 2. Rules

### When to Use Rules
- Coding style preferences
- Project conventions
- Response formatting guidelines
- Cross-cutting concerns
- Behavioral guidelines that apply across conversations

### Rule Structure
```markdown
---
trigger: [always_on | manual | model_decision | glob]
glob: "*.js" (if trigger is glob)
---

# Rule Content

Your instructions here using:
- Bullet points
- Numbered lists
- Clear formatting
```

### Activation Modes

**1. Always On**
```yaml
---
trigger: always_on
---
```
Applied to every conversation.

**2. Manual**
```yaml
---
trigger: manual
---
```
Activated via `@rule-name` mention.

**3. Model Decision**
```yaml
---
trigger: model_decision
---
```
Cascade decides based on natural language description.

**4. Glob Pattern**
```yaml
---
trigger: glob
glob: "src/**/*.ts"
---
```
Applied to files matching the pattern.

### Rule Locations
- **Global**: `~/.codeium/windsurf/rules/` (all workspaces)
- **Workspace**: `.windsurf/rules/` (current project)
- **Subdirectories**: `.windsurf/rules/` in any subdirectory

### Creating a Rule

**Via UI:**
1. Click customizations menu (three dots in Cascade panel)
2. Navigate to Rules section
3. Click `+ Global` or `+ Workspace`

**Manually:**
```bash
# Create workspace rule
mkdir -p .windsurf/rules
cat > .windsurf/rules/my-rule.md << 'EOF'
---
trigger: always_on
---

# My Rule

- Use early returns
- Add documentation for new functions
EOF
```

### Rule Best Practices
- Keep rules simple and specific
- Use bullet points and markdown formatting
- Avoid generic rules (e.g., "write good code")
- Use XML tags to group related rules
- Limit to 12,000 characters per file

## 3. Workflows

### When to Use Workflows
- Repeatable sequences of steps
- Deployment procedures
- PR review processes
- Code formatting routines
- Any task with a defined sequence

### Workflow Structure
```markdown
---
description: Brief description of workflow purpose
---

## Step 1: First Action
Instructions for step 1

// turbo (optional - allows auto-run for this step)
```bash
command to run
```

## Step 2: Second Action
Instructions for step 2

...
```

### Workflow Features

**Calling Other Workflows:**
```markdown
## Step 3: Run Sub-Workflow
Execute /other-workflow to complete this step
```

**Auto-Execution with // turbo:**
```markdown
// turbo
```bash
git status
```
```
Commands marked with `// turbo` can auto-run if safe.

### Workflow Locations
- **Workspace**: `.windsurf/workflows/` (current project)
- **Subdirectories**: `.windsurf/workflows/` in any subdirectory
- **Git root**: Searches up to git root

### Creating a Workflow

**Via UI:**
1. Click customizations menu in Cascade
2. Navigate to Workflows section
3. Click `+ Workflow`

**Manually:**
```bash
mkdir -p .windsurf/workflows
cat > .windsurf/workflows/deploy.md << 'EOF'
---
description: Deploy application to production
---

## Step 1: Run Tests
Execute all tests before deployment

## Step 2: Build
Create production build

## Step 3: Deploy
Deploy to production server
EOF
```

**Generate with Cascade:**
Ask Cascade: "Create a workflow for [task description]"

### Invoking Workflows
Use slash command: `/workflow-name`

### Workflow Best Practices
- Clear step-by-step instructions
- Use `// turbo` for safe auto-run commands
- Include error handling steps
- Reference other workflows when appropriate
- Limit to 12,000 characters per file

## 4. AGENTS.md

### When to Use AGENTS.md
- Directory-specific conventions
- Location-based instructions
- Component guidelines
- Module-specific rules
- Automatic scoping based on file location

### AGENTS.md Structure
```markdown
# Component Guidelines

When working with files in this directory:

- Use functional components with hooks
- Follow naming convention: ComponentName.tsx
- Each component needs ComponentName.test.tsx
- Use CSS modules: ComponentName.module.css
- Export as named exports, not default

## File Structure

Each component folder should contain:
- Main component file
- Test file
- Styles file (if needed)
- index.ts for re-exports
```

### AGENTS.md Scoping

**Root directory**: Applies globally to all files
**Subdirectories**: Applies only to that directory and children

Example structure:
```
project/
├── AGENTS.md (global instructions)
├── frontend/
│   ├── AGENTS.md (frontend-specific)
│   └── components/
│       └── AGENTS.md (component-specific)
└── backend/
    └── AGENTS.md (backend-specific)
```

### Creating AGENTS.md

Simply create a file named `AGENTS.md` or `agents.md` in any directory:

```bash
cat > frontend/components/AGENTS.md << 'EOF'
# Component Guidelines

- Use functional components with hooks
- Follow naming: ComponentName.tsx
- Include tests: ComponentName.test.tsx
- Use CSS modules
EOF
```

### AGENTS.md Best Practices
- Keep instructions focused on the directory's purpose
- Use clear formatting (bullets, headers, code blocks)
- Be specific with concrete examples
- Avoid redundancy (inherits from parent directories)
- No frontmatter required (plain markdown)

## Comparison Matrix

| Feature | Skills | Rules | Workflows | AGENTS.md |
|---------|--------|-------|-----------|-----------|
| **Format** | Folder + SKILL.md | Single .md file | Single .md file | Single .md file |
| **Frontmatter** | Required (YAML) | Required (YAML) | Required (YAML) | None |
| **Resources** | Yes (scripts/refs/assets) | No | No | No |
| **Invocation** | Auto or @mention | Based on trigger | /slash-command | Automatic by location |
| **Scoping** | Global/workspace | Global/workspace/glob | Workspace | Directory-based |
| **Best For** | Complex tasks | Behavior/style | Step sequences | Location rules |
| **Size Limit** | Unlimited (split files) | 12,000 chars | 12,000 chars | No limit |

## Common Workflows

### Creating a New Skill
1. Understand the use case with concrete examples
2. Plan reusable resources (scripts, references, assets)
3. Run `init_skill.py` to create structure
4. Edit SKILL.md and add resources
5. Test the skill with real tasks
6. Iterate based on usage

### Creating a New Rule
1. Identify the behavioral guideline needed
2. Choose activation mode (always_on, manual, model_decision, glob)
3. Create rule file in `.windsurf/rules/`
4. Write clear, concise instructions
5. Test with relevant files/conversations

### Creating a New Workflow
1. Define the sequence of steps
2. Create workflow file in `.windsurf/workflows/`
3. Add description in frontmatter
4. Write step-by-step instructions
5. Mark safe commands with `// turbo`
6. Test with `/workflow-name`

### Creating AGENTS.md
1. Identify directory-specific conventions
2. Create `AGENTS.md` in target directory
3. Write focused instructions for that directory
4. Test by working with files in that directory

## References

For detailed guidance on specific topics, see:
- `references/skill-creation-guide.md` - Deep dive on skill design patterns
- `references/rule-patterns.md` - Common rule patterns and examples
- `references/workflow-patterns.md` - Workflow design patterns
- `references/troubleshooting.md` - Common issues and solutions
