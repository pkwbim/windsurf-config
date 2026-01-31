#!/usr/bin/env python3
"""
Quick workflow creator for Windsurf

Usage:
    create_workflow.py <workflow-name>

Examples:
    create_workflow.py deploy-staging
    create_workflow.py code-review
"""

import sys
from pathlib import Path

WORKFLOW_TEMPLATE = """---
description: {description}
---

## Step 1: {step1_title}

TODO - Add instructions for first step

Example:
```bash
git status
```

## Step 2: {step2_title}

TODO - Add instructions for second step

## Step 3: {step3_title}

TODO - Add instructions for final step

---

## Notes

- Use // turbo before code blocks to enable auto-execution for safe commands
- Call other workflows with /{workflow_name}
- Add conditional logic with "If X then Y" sections
"""

def title_case(name):
    """Convert hyphenated name to Title Case"""
    return ' '.join(word.capitalize() for word in name.split('-'))

def create_workflow(workflow_name):
    """Create a new workflow file"""
    
    base_path = Path('.windsurf') / 'workflows'
    base_path.mkdir(parents=True, exist_ok=True)
    
    workflow_file = base_path / f'{workflow_name}.md'
    
    # Check if exists
    if workflow_file.exists():
        print(f"❌ Workflow file already exists: {workflow_file}")
        return False
    
    # Create workflow file
    workflow_title = title_case(workflow_name)
    content = WORKFLOW_TEMPLATE.format(
        workflow_name=workflow_name,
        description=f"TODO - Describe what this workflow does",
        step1_title="First Action",
        step2_title="Second Action",
        step3_title="Final Action"
    )
    
    workflow_file.write_text(content)
    print(f"✅ Created workflow: {workflow_file}")
    
    print(f"\n✨ Workflow '{workflow_name}' created successfully!")
    print(f"\nInvoke with: /{workflow_name}")
    
    print(f"\nNext steps:")
    print(f"1. Edit {workflow_file}")
    print(f"2. Update the description in frontmatter")
    print(f"3. Replace TODO sections with actual steps")
    print(f"4. Add // turbo for safe auto-executable commands")
    print(f"5. Test with /{workflow_name}")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: create_workflow.py <workflow-name>")
        print("\nExamples:")
        print("  create_workflow.py deploy-staging")
        print("  create_workflow.py code-review")
        print("  create_workflow.py run-tests")
        sys.exit(1)
    
    workflow_name = sys.argv[1]
    
    if not create_workflow(workflow_name):
        sys.exit(1)

if __name__ == "__main__":
    main()
