#!/usr/bin/env python3
"""
Quick AGENTS.md creator for Windsurf

Usage:
    create_agents_md.py <directory> [--template <type>]

Templates: component, backend, frontend, docs

Examples:
    create_agents_md.py src/components --template component
    create_agents_md.py backend/api --template backend
    create_agents_md.py .
"""

import sys
from pathlib import Path

TEMPLATES = {
    'component': """# Component Guidelines

When working with components in this directory:

- Use functional components with hooks
- Follow naming convention: ComponentName.tsx
- Each component needs ComponentName.test.tsx
- Use CSS modules: ComponentName.module.css
- Export as named exports, not default exports

## File Structure

Each component folder should contain:
- Main component file
- Test file
- Styles file (if needed)
- index.ts for re-exports

## Example

```typescript
// UserProfile.tsx
export const UserProfile = ({ userId }: Props) => {
  // Component logic
}
```
""",
    'backend': """# Backend API Guidelines

When working with backend code in this directory:

- Follow RESTful conventions
- Use async/await for asynchronous operations
- Implement proper error handling
- Add input validation
- Include unit tests for all endpoints

## File Organization

- Routes: Define API endpoints
- Controllers: Handle business logic
- Services: Interact with database/external APIs
- Models: Define data structures

## Example

```typescript
// users.controller.ts
export async function getUser(req: Request, res: Response) {
  try {
    const user = await userService.findById(req.params.id)
    res.json(user)
  } catch (error) {
    res.status(500).json({ error: error.message })
  }
}
```
""",
    'frontend': """# Frontend Guidelines

When working with frontend code in this directory:

- Use TypeScript for type safety
- Follow component composition patterns
- Implement responsive design
- Use modern CSS (Grid, Flexbox)
- Optimize for performance

## State Management

- Use React hooks for local state
- Use context for shared state
- Consider Redux/Zustand for complex state

## Styling

- Use CSS modules or styled-components
- Follow mobile-first approach
- Maintain consistent spacing and typography
""",
    'docs': """# Documentation Guidelines

When working with documentation in this directory:

- Use clear, concise language
- Include code examples
- Add diagrams where helpful
- Keep documentation up-to-date with code changes

## Structure

- README.md: Overview and quick start
- API.md: API documentation
- GUIDE.md: Detailed guides
- CHANGELOG.md: Version history

## Writing Style

- Use active voice
- Write in present tense
- Include practical examples
- Link to related documentation
""",
    'generic': """# Directory Guidelines

When working with files in this directory:

TODO - Add specific guidelines for this directory

## Conventions

- TODO - Naming conventions
- TODO - File organization
- TODO - Code style

## Best Practices

- TODO - Best practices specific to this directory
- TODO - Common patterns to follow
- TODO - Things to avoid
"""
}

def create_agents_md(directory, template_type='generic'):
    """Create AGENTS.md file in specified directory"""
    
    if template_type not in TEMPLATES:
        print(f"❌ Invalid template type: {template_type}")
        print(f"Valid types: {', '.join(TEMPLATES.keys())}")
        return False
    
    dir_path = Path(directory)
    
    # Create directory if it doesn't exist
    if not dir_path.exists():
        print(f"❌ Directory does not exist: {dir_path}")
        return False
    
    agents_file = dir_path / 'AGENTS.md'
    
    # Check if exists
    if agents_file.exists():
        print(f"❌ AGENTS.md already exists: {agents_file}")
        return False
    
    # Create AGENTS.md
    content = TEMPLATES[template_type]
    agents_file.write_text(content)
    
    print(f"✅ Created AGENTS.md: {agents_file}")
    print(f"\nTemplate: {template_type}")
    print(f"\n✨ AGENTS.md created successfully!")
    
    print(f"\nScope:")
    print(f"- Applies to: {dir_path.absolute()}")
    print(f"- Applies to all subdirectories")
    print(f"- Inherits from parent AGENTS.md files")
    
    print(f"\nNext steps:")
    print(f"1. Edit {agents_file}")
    print(f"2. Customize guidelines for this directory")
    print(f"3. Test by working with files in this directory")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: create_agents_md.py <directory> [--template <type>]")
        print("\nTemplates:")
        print("  component - Component development guidelines")
        print("  backend   - Backend API guidelines")
        print("  frontend  - Frontend development guidelines")
        print("  docs      - Documentation guidelines")
        print("  generic   - Generic template (default)")
        print("\nExamples:")
        print("  create_agents_md.py src/components --template component")
        print("  create_agents_md.py backend/api --template backend")
        print("  create_agents_md.py .")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    # Parse template argument
    template_type = 'generic'
    if '--template' in sys.argv:
        idx = sys.argv.index('--template')
        if idx + 1 < len(sys.argv):
            template_type = sys.argv[idx + 1]
    
    if not create_agents_md(directory, template_type):
        sys.exit(1)

if __name__ == "__main__":
    main()
