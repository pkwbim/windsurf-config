#!/usr/bin/env python3
"""
Quick rule creator for Windsurf

Usage:
    create_rule.py <rule-name> <trigger-type> [--global]

Trigger types: always_on, manual, model_decision, glob

Examples:
    create_rule.py coding-style always_on
    create_rule.py typescript-rules glob --global
    create_rule.py security-check model_decision
"""

import sys
from pathlib import Path

RULE_TEMPLATES = {
    'always_on': """---
trigger: always_on
---

# {rule_title}

TODO - Add your always-on rules here. These apply to all conversations.

Example:
- Use early returns when possible
- Add documentation for new functions
- Prefer const over let
""",
    'manual': """---
trigger: manual
---

# {rule_title}

TODO - Add your manual rules here. Activate with @{rule_name}

Example:
- Follow specific coding pattern
- Use particular framework conventions
- Apply special formatting rules
""",
    'model_decision': """---
trigger: model_decision
---

# {rule_title}

TODO - Add your context-dependent rules here. Cascade decides when to apply.

Example:
When working with financial data:
- Use Decimal type for currency
- Round to 2 decimal places
- Store amounts in cents
""",
    'glob': """---
trigger: glob
glob: "**/*.{rule_name_ext}"
---

# {rule_title}

TODO - Add your file-specific rules here. Update the glob pattern above.

Example glob patterns:
- "*.js" - JS files in current directory
- "**/*.ts" - All TypeScript files
- "src/**/*.vue" - Vue files in src/

Example rules:
- Use specific syntax for this file type
- Follow framework conventions
- Apply linting rules
"""
}

def title_case(name):
    """Convert hyphenated name to Title Case"""
    return ' '.join(word.capitalize() for word in name.split('-'))

def create_rule(rule_name, trigger_type, is_global=False):
    """Create a new rule file"""
    
    if trigger_type not in RULE_TEMPLATES:
        print(f"❌ Invalid trigger type: {trigger_type}")
        print(f"Valid types: {', '.join(RULE_TEMPLATES.keys())}")
        return False
    
    # Determine base path
    if is_global:
        base_path = Path.home() / '.codeium' / 'windsurf' / 'rules'
    else:
        base_path = Path('.windsurf') / 'rules'
    
    base_path.mkdir(parents=True, exist_ok=True)
    rule_file = base_path / f'{rule_name}.md'
    
    # Check if exists
    if rule_file.exists():
        print(f"❌ Rule file already exists: {rule_file}")
        return False
    
    # Create rule file
    rule_title = title_case(rule_name)
    content = RULE_TEMPLATES[trigger_type].format(
        rule_name=rule_name,
        rule_title=rule_title,
        rule_name_ext='ts'  # Default extension for glob example
    )
    
    rule_file.write_text(content)
    print(f"✅ Created rule: {rule_file}")
    
    print(f"\n✨ Rule '{rule_name}' created successfully!")
    print(f"\nTrigger type: {trigger_type}")
    
    if trigger_type == 'always_on':
        print("This rule will apply to all conversations")
    elif trigger_type == 'manual':
        print(f"Activate with: @{rule_name}")
    elif trigger_type == 'model_decision':
        print("Cascade will decide when to apply this rule")
    elif trigger_type == 'glob':
        print("Remember to update the glob pattern in the frontmatter")
    
    print(f"\nNext steps:")
    print(f"1. Edit {rule_file}")
    print(f"2. Replace TODO sections with actual rules")
    print(f"3. Test the rule in Cascade")
    
    return True

def main():
    if len(sys.argv) < 3:
        print("Usage: create_rule.py <rule-name> <trigger-type> [--global]")
        print("\nTrigger types:")
        print("  always_on      - Always active")
        print("  manual         - Activate with @mention")
        print("  model_decision - Cascade decides")
        print("  glob           - File pattern matching")
        print("\nExamples:")
        print("  create_rule.py coding-style always_on")
        print("  create_rule.py typescript-rules glob --global")
        sys.exit(1)
    
    rule_name = sys.argv[1]
    trigger_type = sys.argv[2]
    is_global = '--global' in sys.argv
    
    if not create_rule(rule_name, trigger_type, is_global):
        sys.exit(1)

if __name__ == "__main__":
    main()
