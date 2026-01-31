# Rule Patterns and Examples

## Common Rule Patterns

### 1. Coding Style Rules

**Always On Pattern**:
```markdown
---
trigger: always_on
---

# Coding Guidelines

- Use early returns when possible
- Add documentation for new functions and classes
- Prefer const over let
- Use descriptive variable names
```

**Glob Pattern for Specific Files**:
```markdown
---
trigger: glob
glob: "**/*.ts"
---

# TypeScript Guidelines

- Use explicit types, avoid `any`
- Define interfaces for object shapes
- Use enums for fixed sets of values
```

### 2. Project Convention Rules

```markdown
---
trigger: always_on
---

# Project Conventions

## File Organization
- Place components in `src/components/`
- Place utilities in `src/utils/`
- Place types in `src/types/`

## Naming Conventions
- Components: PascalCase (e.g., `UserProfile.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

## Testing
- Test files: `*.test.ts` or `*.spec.ts`
- Place tests next to source files
- Aim for >80% coverage
```

### 3. Response Formatting Rules

```markdown
---
trigger: always_on
---

# Response Format

When providing code explanations:
1. Start with a brief summary
2. Show the code with inline comments
3. Explain key concepts
4. Provide usage examples
5. Note any gotchas or edge cases

Use markdown code blocks with language identifiers.
```

### 4. Framework-Specific Rules

```markdown
---
trigger: glob
glob: "src/**/*.vue"
---

# Vue 3 Component Guidelines

- Use Composition API with `<script setup>`
- Define props with TypeScript types
- Use `ref` for reactive primitives
- Use `reactive` for reactive objects
- Emit events with `defineEmits`
- Expose methods with `defineExpose`

## Example Structure
\`\`\`vue
<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ title: string }>()
const count = ref(0)
</script>
\`\`\`
```

### 5. Domain-Specific Rules

```markdown
---
trigger: model_decision
---

# Financial Calculations

When working with financial data:

- Use Decimal type for currency (never float)
- Round to 2 decimal places for display
- Store amounts in cents (integer)
- Always specify currency code (USD, EUR, etc.)
- Include timezone for timestamps
- Validate amounts are non-negative where appropriate
```

### 6. Security Rules

```markdown
---
trigger: always_on
---

# Security Guidelines

<security_rules>
- Never hardcode API keys or secrets
- Use environment variables for sensitive data
- Sanitize user input before database queries
- Use parameterized queries (prevent SQL injection)
- Validate and sanitize file uploads
- Implement rate limiting on API endpoints
- Use HTTPS for all external communications
</security_rules>
```

### 7. Documentation Rules

```markdown
---
trigger: glob
glob: "**/*.{ts,js}"
---

# Documentation Standards

## Function Documentation
\`\`\`typescript
/**
 * Brief description of what the function does
 * 
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws Description of errors thrown
 * 
 * @example
 * const result = myFunction('input')
 */
\`\`\`

## Class Documentation
- Document purpose and responsibilities
- Document public methods
- Include usage examples
```

### 8. Git Commit Rules

```markdown
---
trigger: manual
---

# Git Commit Message Format

Use conventional commits format:

\`\`\`
<type>(<scope>): <subject>

<body>

<footer>
\`\`\`

**Types**:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes (formatting)
- refactor: Code refactoring
- test: Adding or updating tests
- chore: Maintenance tasks

**Example**:
\`\`\`
feat(auth): add OAuth2 login support

Implemented OAuth2 authentication flow with Google provider.
Added token refresh mechanism and session management.

Closes #123
\`\`\`
```

## XML Tag Grouping

Group related rules with XML tags for better organization:

```markdown
---
trigger: always_on
---

<coding_style>
- Use early returns
- Prefer const over let
- Use descriptive names
</coding_style>

<testing_requirements>
- Write unit tests for all functions
- Include integration tests for APIs
- Aim for >80% coverage
</testing_requirements>

<documentation>
- Add JSDoc comments for public APIs
- Include usage examples
- Document edge cases
</documentation>
```

## Activation Mode Selection Guide

### Use Always On When:
- Rules apply to all conversations
- General coding standards
- Project-wide conventions
- Security guidelines

### Use Manual When:
- Rules for specific tasks
- Optional guidelines
- Context-specific instructions
- User explicitly invokes

### Use Model Decision When:
- Rules for specific domains
- Context-dependent guidelines
- Cascade should decide relevance

### Use Glob When:
- File type-specific rules
- Language-specific guidelines
- Directory-specific conventions

## Best Practices

### 1. Keep Rules Concise
**Bad**:
```markdown
When you are writing code, you should always make sure to use early returns whenever it is possible to do so, because this makes the code more readable and easier to understand for other developers who might be working on the codebase in the future.
```

**Good**:
```markdown
- Use early returns when possible
```

### 2. Use Structured Formatting
**Bad**:
```markdown
Use TypeScript types and avoid any and prefer interfaces and use enums.
```

**Good**:
```markdown
# TypeScript Guidelines
- Use explicit types
- Avoid `any`
- Prefer interfaces for object shapes
- Use enums for fixed value sets
```

### 3. Provide Examples
**Bad**:
```markdown
Use proper naming conventions.
```

**Good**:
```markdown
# Naming Conventions
- Components: `UserProfile.tsx` (PascalCase)
- Utilities: `formatDate.ts` (camelCase)
- Constants: `API_BASE_URL` (UPPER_SNAKE_CASE)
```

### 4. Avoid Generic Rules
**Don't include**:
- "Write good code"
- "Follow best practices"
- "Be consistent"

**Do include**:
- Specific conventions
- Concrete examples
- Project-specific requirements

### 5. Use Appropriate Scope
- **Global rules**: Team-wide standards
- **Workspace rules**: Project-specific conventions
- **Subdirectory rules**: Module-specific guidelines

## Testing Your Rules

1. **Test activation**: Verify rule triggers correctly
2. **Check relevance**: Ensure rule applies when needed
3. **Validate behavior**: Confirm Cascade follows the rule
4. **Iterate**: Refine based on actual usage
