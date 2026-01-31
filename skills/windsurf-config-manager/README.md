# Windsurf Configuration Manager Skill

A comprehensive skill for creating and managing all types of Windsurf configuration files: Skills, Rules, Workflows, and AGENTS.md.

## What This Skill Provides

- **Quick Decision Guide**: Choose the right configuration type for your needs
- **Detailed Documentation**: Complete guides for each configuration type
- **Helper Scripts**: Automated creation tools for all config types
- **Templates**: Ready-to-use templates for quick setup
- **Troubleshooting**: Common issues and solutions

## Structure

```
windsurf-config-manager/
├── SKILL.md                          # Main skill file with overview
├── scripts/                          # Helper scripts
│   ├── create_skill.py              # Create new skills
│   ├── create_rule.py               # Create new rules
│   ├── create_workflow.py           # Create new workflows
│   └── create_agents_md.py          # Create AGENTS.md files
├── references/                       # Detailed guides
│   ├── skill-creation-guide.md      # Deep dive on skills
│   ├── rule-patterns.md             # Rule patterns and examples
│   ├── workflow-patterns.md         # Workflow design patterns
│   └── troubleshooting.md           # Common issues
└── assets/                           # Templates
    ├── skill-template.md            # Basic skill template
    ├── rule-template.md             # Basic rule template
    └── workflow-template.md         # Basic workflow template
```

## Usage

### Via Cascade

Simply mention what you want to create:
- "Create a skill for deployment"
- "I need a rule for TypeScript files"
- "Help me create a workflow for testing"
- "Set up AGENTS.md for my components directory"

### Via Scripts

```bash
# Create a new skill
python3 scripts/create_skill.py my-skill-name

# Create a new rule
python3 scripts/create_rule.py my-rule always_on

# Create a new workflow
python3 scripts/create_workflow.py my-workflow

# Create AGENTS.md
python3 scripts/create_agents_md.py src/components --template component
```

## Quick Reference

| Need | Use | Invoke With |
|------|-----|-------------|
| Complex task with resources | Skill | Auto or @skill-name |
| Behavioral guidelines | Rule | Based on trigger |
| Step-by-step process | Workflow | /workflow-name |
| Directory conventions | AGENTS.md | Automatic |

## When to Use This Skill

Cascade will automatically invoke this skill when you:
- Want to create or modify Windsurf configurations
- Need guidance on Skills, Rules, Workflows, or AGENTS.md
- Ask about configuration file structure
- Need help choosing the right configuration type

You can also manually invoke with: `@windsurf-config-manager`
