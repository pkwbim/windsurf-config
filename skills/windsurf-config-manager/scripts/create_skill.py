#!/usr/bin/env python3
"""
Quick skill creator for Windsurf

Usage:
    create_skill.py <skill-name> [--global]

Examples:
    create_skill.py my-deployment-skill
    create_skill.py code-review --global
"""

import sys
from pathlib import Path

SKILL_TEMPLATE = """---
name: {skill_name}
description: TODO - Describe what this skill does and when to use it. Include specific triggers, file types, and use cases.
---

# {skill_title}

## Overview

TODO - Brief explanation of what this skill enables

## Quick Start

TODO - Basic usage example

## Core Functionality

TODO - Main features and capabilities

## Resources

This skill includes:
- `scripts/` - Executable helper scripts
- `references/` - Detailed documentation
- `assets/` - Templates and resources

Delete any unused directories.
"""

def title_case(name):
    """Convert hyphenated name to Title Case"""
    return ' '.join(word.capitalize() for word in name.split('-'))

def create_skill(skill_name, is_global=False):
    """Create a new skill directory with basic structure"""
    
    # Determine base path
    if is_global:
        base_path = Path.home() / '.codeium' / 'windsurf' / 'skills'
    else:
        base_path = Path('.windsurf') / 'skills'
    
    skill_dir = base_path / skill_name
    
    # Check if exists
    if skill_dir.exists():
        print(f"❌ Skill directory already exists: {skill_dir}")
        return False
    
    # Create directory
    skill_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created skill directory: {skill_dir}")
    
    # Create SKILL.md
    skill_title = title_case(skill_name)
    content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )
    
    (skill_dir / 'SKILL.md').write_text(content)
    print(f"✅ Created SKILL.md")
    
    # Create resource directories
    (skill_dir / 'scripts').mkdir(exist_ok=True)
    (skill_dir / 'references').mkdir(exist_ok=True)
    (skill_dir / 'assets').mkdir(exist_ok=True)
    print(f"✅ Created resource directories")
    
    print(f"\n✨ Skill '{skill_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"1. Edit {skill_dir / 'SKILL.md'}")
    print(f"2. Add resources to scripts/, references/, or assets/")
    print(f"3. Update the description field with specific triggers")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: create_skill.py <skill-name> [--global]")
        sys.exit(1)
    
    skill_name = sys.argv[1]
    is_global = '--global' in sys.argv
    
    if not create_skill(skill_name, is_global):
        sys.exit(1)

if __name__ == "__main__":
    main()
