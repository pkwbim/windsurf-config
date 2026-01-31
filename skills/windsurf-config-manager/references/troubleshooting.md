# Troubleshooting Windsurf Configurations

## Skills Issues

### Skill Not Triggering Automatically

**Symptoms**: Skill doesn't invoke when expected

**Causes & Solutions**:

1. **Vague description**
   - **Fix**: Make description more specific with clear triggers
   - **Example**: Instead of "Helps with documents", use "Use when working with .docx files for creating, editing, or analyzing documents"

2. **Missing trigger keywords**
   - **Fix**: Include file types, actions, and contexts in description
   - **Example**: Add "Use when user mentions: PDF, document conversion, file merging"

3. **Skill not in correct location**
   - **Fix**: Verify skill is in `.windsurf/skills/` (workspace) or `~/.codeium/windsurf/skills/` (global)

4. **SKILL.md frontmatter errors**
   - **Fix**: Verify YAML frontmatter is valid:
   ```yaml
   ---
   name: skill-name
   description: Clear description here
   ---
   ```

### Skill Resources Not Loading

**Symptoms**: Scripts or references not accessible

**Causes & Solutions**:

1. **Incorrect file paths**
   - **Fix**: Use relative paths from skill directory
   - **Example**: `references/api_docs.md` not `/references/api_docs.md`

2. **Missing references in SKILL.md**
   - **Fix**: Explicitly mention resource files in SKILL.md
   - **Example**: "See `references/schema.md` for database schema"

3. **File permissions**
   - **Fix**: Ensure scripts are executable
   ```bash
   chmod +x scripts/my_script.py
   ```

### Skill Context Too Large

**Symptoms**: Skill loads too much into context

**Causes & Solutions**:

1. **SKILL.md too long**
   - **Fix**: Split content into reference files
   - **Keep**: Core workflow and navigation in SKILL.md
   - **Move**: Detailed docs to `references/`

2. **Loading all references at once**
   - **Fix**: Use domain-specific reference files
   - **Example**: Split into `references/aws.md`, `references/gcp.md`

## Rules Issues

### Rule Not Activating

**Symptoms**: Rule doesn't apply when expected

**Causes & Solutions**:

1. **Wrong trigger mode**
   - **Fix**: Verify trigger matches use case:
   - `always_on`: For all conversations
   - `manual`: Requires @mention
   - `model_decision`: Cascade decides
   - `glob`: For specific file patterns

2. **Glob pattern incorrect**
   - **Fix**: Test glob pattern
   - **Examples**:
     - `*.js` - JS files in current directory only
     - `**/*.js` - All JS files recursively
     - `src/**/*.ts` - TypeScript files in src/

3. **Rule file not discovered**
   - **Fix**: Check rule location:
   - Global: `~/.codeium/windsurf/rules/`
   - Workspace: `.windsurf/rules/`
   - Verify file has `.md` extension

4. **Frontmatter syntax error**
   - **Fix**: Verify YAML syntax:
   ```yaml
   ---
   trigger: always_on
   ---
   ```

### Rule Conflicts

**Symptoms**: Rules contradict each other

**Causes & Solutions**:

1. **Multiple always_on rules with conflicting guidance**
   - **Fix**: Consolidate related rules into one file
   - **Fix**: Use more specific triggers (glob or model_decision)

2. **Global vs workspace rule conflict**
   - **Fix**: Workspace rules should be more specific
   - **Fix**: Document which takes precedence in your team

### Rule Too Generic

**Symptoms**: Rule doesn't provide useful guidance

**Causes & Solutions**:

1. **Vague instructions**
   - **Bad**: "Write good code"
   - **Good**: "Use early returns when possible"

2. **Missing examples**
   - **Fix**: Add concrete examples
   ```markdown
   # Naming Conventions
   - Components: `UserProfile.tsx` (PascalCase)
   - Utilities: `formatDate.ts` (camelCase)
   ```

## Workflows Issues

### Workflow Not Found

**Symptoms**: `/workflow-name` doesn't work

**Causes & Solutions**:

1. **Workflow not in correct location**
   - **Fix**: Place in `.windsurf/workflows/`
   - **Fix**: Ensure file has `.md` extension

2. **Filename doesn't match command**
   - **Fix**: Filename should match slash command
   - **Example**: `/deploy` requires `deploy.md`

3. **Workflow not discovered**
   - **Fix**: Restart Windsurf to refresh workflow list
   - **Fix**: Check file is not in `.gitignore`

### Workflow Steps Unclear

**Symptoms**: Cascade doesn't follow workflow correctly

**Causes & Solutions**:

1. **Vague instructions**
   - **Fix**: Use specific, actionable language
   - **Bad**: "Do the deployment"
   - **Good**: "Execute `./deploy.sh production`"

2. **Missing context**
   - **Fix**: Explain why each step is needed
   - **Fix**: Include expected outcomes

3. **No error handling**
   - **Fix**: Add "If X fails" sections
   ```markdown
   ## Step 2: Build
   ```bash
   npm run build
   ```
   
   **If build fails:**
   - Check for TypeScript errors
   - Verify dependencies installed
   ```

### Auto-Execution Not Working

**Symptoms**: Commands marked with // turbo don't auto-run

**Causes & Solutions**:

1. **Command is unsafe**
   - **Fix**: Only mark truly safe commands with // turbo
   - **Safe**: `git status`, `npm test`, `cat file.txt`
   - **Unsafe**: `rm -rf`, `git push`, `npm publish`

2. **Syntax error**
   - **Fix**: Ensure // turbo is on its own line before code block
   ```markdown
   // turbo
   ```bash
   git status
   ```
   ```

## AGENTS.md Issues

### AGENTS.md Not Applying

**Symptoms**: Instructions not followed for directory files

**Causes & Solutions**:

1. **File not named correctly**
   - **Fix**: Must be `AGENTS.md` or `agents.md` (case-insensitive)

2. **Working in wrong directory**
   - **Fix**: AGENTS.md only applies to its directory and subdirectories
   - **Fix**: Verify you're working with files in the correct location

3. **Instructions too vague**
   - **Fix**: Be specific with concrete examples
   - **Bad**: "Follow conventions"
   - **Good**: "Use PascalCase for component names: `UserProfile.tsx`"

### AGENTS.md Conflicts

**Symptoms**: Multiple AGENTS.md files with conflicting rules

**Causes & Solutions**:

1. **Parent and child directories conflict**
   - **Fix**: Child directory AGENTS.md should be more specific
   - **Fix**: Avoid repeating parent instructions

2. **Redundant instructions**
   - **Fix**: Remove duplicate instructions from child directories
   - **Remember**: Child directories inherit from parent

## General Issues

### Configuration Not Taking Effect

**Symptoms**: Changes to config files not reflected

**Causes & Solutions**:

1. **Need to restart Windsurf**
   - **Fix**: Restart Windsurf to reload configurations

2. **File encoding issues**
   - **Fix**: Ensure files are UTF-8 encoded
   - **Fix**: Check for BOM (Byte Order Mark) and remove

3. **Syntax errors in frontmatter**
   - **Fix**: Validate YAML syntax
   - **Tool**: Use online YAML validator

### Size Limit Exceeded

**Symptoms**: Error about file size

**Causes & Solutions**:

1. **Rule or workflow too large**
   - **Limit**: 12,000 characters per file
   - **Fix**: Split into multiple files
   - **Fix**: Remove unnecessary content

2. **Skill too large**
   - **Fix**: Split SKILL.md into reference files
   - **Fix**: Move detailed docs to `references/`

### Discovery Issues

**Symptoms**: Configurations not showing up

**Causes & Solutions**:

1. **Wrong directory structure**
   - **Fix**: Verify correct paths:
   - Skills: `.windsurf/skills/<name>/SKILL.md`
   - Rules: `.windsurf/rules/<name>.md`
   - Workflows: `.windsurf/workflows/<name>.md`
   - AGENTS.md: Any directory

2. **Git repository structure**
   - **Fix**: For git repos, Windsurf searches up to git root
   - **Fix**: Ensure configs are within git repository

3. **Multiple workspaces**
   - **Fix**: Check which workspace is active
   - **Fix**: Configs are workspace-specific

## Debugging Tips

### 1. Check File Locations
```bash
# List all skills
find . -name "SKILL.md" -type f

# List all rules
find . -path "*/.windsurf/rules/*.md" -type f

# List all workflows
find . -path "*/.windsurf/workflows/*.md" -type f

# List all AGENTS.md
find . -name "AGENTS.md" -o -name "agents.md"
```

### 2. Validate YAML Frontmatter
```bash
# Extract and validate frontmatter
head -n 10 .windsurf/rules/my-rule.md
```

### 3. Test Glob Patterns
```bash
# Test if files match glob pattern
ls src/**/*.ts
```

### 4. Check Permissions
```bash
# Verify script is executable
ls -l scripts/my_script.py
```

### 5. View Cascade Logs
Check Windsurf logs for errors:
- Help → Toggle Developer Tools → Console

## Getting Help

If issues persist:

1. **Check official docs**: https://docs.windsurf.com
2. **Verify file structure**: Compare with working examples
3. **Test with minimal config**: Create simple test case
4. **Check for updates**: Ensure Windsurf is up to date
5. **Review error messages**: Look for specific error details
