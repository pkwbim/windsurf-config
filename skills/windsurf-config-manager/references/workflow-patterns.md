# Workflow Design Patterns

## Workflow Structure

Basic workflow template:
```markdown
---
description: Brief description of workflow purpose
---

## Step 1: First Action
Clear instructions for what to do

## Step 2: Second Action
Clear instructions for what to do

## Step 3: Final Action
Clear instructions for what to do
```

## Pattern 1: Linear Workflow

**Use for**: Simple sequential processes

```markdown
---
description: Deploy application to staging environment
---

## Step 1: Run Tests
Execute all unit and integration tests:
```bash
npm test
```

## Step 2: Build Application
Create production build:
```bash
npm run build
```

## Step 3: Deploy to Staging
Deploy the built application:
```bash
./scripts/deploy-staging.sh
```

## Step 4: Verify Deployment
Check that the deployment was successful:
- Visit staging URL
- Run smoke tests
- Check logs for errors
```

## Pattern 2: Conditional Workflow

**Use for**: Processes with decision points

```markdown
---
description: Handle pull request review
---

## Step 1: Review Code Changes
Examine the PR for:
- Code quality
- Test coverage
- Documentation updates

## Step 2: Decision Point

**If changes needed:**
- Add review comments
- Request changes
- Stop here

**If approved:**
- Continue to Step 3

## Step 3: Approve and Merge
- Approve the PR
- Merge to main branch
- Delete feature branch
```

## Pattern 3: Checklist Workflow

**Use for**: Quality assurance processes

```markdown
---
description: Pre-deployment checklist
---

## Pre-Deployment Verification

Run through this checklist before deploying:

### Code Quality
- [ ] All tests passing
- [ ] No linting errors
- [ ] Code reviewed and approved
- [ ] No TODO comments in critical paths

### Documentation
- [ ] README updated
- [ ] API docs updated
- [ ] Changelog updated
- [ ] Migration guide (if needed)

### Infrastructure
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Monitoring alerts configured
- [ ] Rollback plan documented

### Security
- [ ] Dependencies updated
- [ ] Security scan passed
- [ ] Secrets rotated (if needed)
- [ ] Access controls verified

## Final Step: Deploy
Once all items checked, proceed with deployment.
```

## Pattern 4: Multi-Path Workflow

**Use for**: Different approaches to same goal

```markdown
---
description: Fix production bug
---

## Step 1: Assess Severity

Determine bug severity:
- **Critical**: Affects all users, system down
- **High**: Affects many users, major feature broken
- **Medium**: Affects some users, workaround exists
- **Low**: Minor issue, cosmetic

## Step 2: Choose Response Path

### For Critical Bugs
1. Immediately notify team
2. Create hotfix branch from production
3. Implement minimal fix
4. Deploy directly to production
5. Follow up with proper fix

### For High Priority Bugs
1. Create fix branch from main
2. Implement fix with tests
3. Fast-track PR review
4. Deploy to staging first
5. Deploy to production after verification

### For Medium/Low Priority Bugs
1. Create fix branch from main
2. Implement comprehensive fix
3. Add tests and documentation
4. Normal PR review process
5. Deploy in next release cycle
```

## Pattern 5: Nested Workflow

**Use for**: Complex processes with sub-workflows

```markdown
---
description: Complete feature development cycle
---

## Step 1: Planning
Execute /plan workflow to create feature specification

## Step 2: Development
Execute /build workflow to implement the feature

## Step 3: Testing
Execute /integration workflow to run full test suite

## Step 4: Review
Execute /review workflow to conduct code review

## Step 5: Deployment
Execute /deploy workflow to release the feature
```

## Pattern 6: Interactive Workflow

**Use for**: Processes requiring user input

```markdown
---
description: Create new API endpoint
---

## Step 1: Gather Requirements
Ask the user:
- What is the endpoint path?
- What HTTP method (GET, POST, PUT, DELETE)?
- What are the request parameters?
- What should the response look like?

Wait for user response before continuing.

## Step 2: Design Implementation
Based on user input, design:
- Route definition
- Controller logic
- Data validation
- Response format

Show design to user for approval.

## Step 3: Implement
Create the following files:
- Route definition in `routes/`
- Controller in `controllers/`
- Tests in `tests/`

## Step 4: Test
Run tests and verify endpoint works as expected.
```

## Pattern 7: Iterative Workflow

**Use for**: Processes that repeat until complete

```markdown
---
description: Refactor legacy code module
---

## Step 1: Identify Target
Select next module to refactor from the list.

## Step 2: Analyze Current Code
Review the module:
- Understand current functionality
- Identify code smells
- Note dependencies

## Step 3: Plan Refactoring
Determine refactoring approach:
- Extract functions
- Simplify logic
- Improve naming
- Add tests

## Step 4: Implement Changes
Make the refactoring changes incrementally.

## Step 5: Verify
Run tests to ensure functionality preserved.

## Step 6: Repeat or Complete
- If more modules remain: Return to Step 1
- If all modules done: Complete workflow
```

## Auto-Execution with // turbo

Mark safe commands for auto-execution:

```markdown
## Step 1: Check Git Status
// turbo
```bash
git status
```

## Step 2: Run Tests
// turbo
```bash
npm test
```

## Step 3: Build Project
// turbo
```bash
npm run build
```
```

**Use // turbo for**:
- Read-only commands (git status, ls, cat)
- Safe build commands
- Test execution
- Status checks

**Don't use // turbo for**:
- Commands that modify files
- Commands that delete data
- Deployment commands
- Commands requiring confirmation

## Workflow Composition

Call other workflows within workflows:

```markdown
---
description: Full release process
---

## Step 1: Prepare Release
Execute /plan to finalize release notes

## Step 2: Run Quality Checks
Execute /integration to run full test suite

## Step 3: Deploy to Staging
Execute /deploy-staging to deploy to staging environment

## Step 4: Verify Staging
Manual verification of staging deployment

## Step 5: Deploy to Production
Execute /deploy-production to release to production

## Step 6: Post-Release
Execute /review to document lessons learned
```

## Best Practices

### 1. Clear Step Titles
**Bad**: "Do the thing"
**Good**: "Run Integration Tests"

### 2. Actionable Instructions
**Bad**: "Make sure everything works"
**Good**: "Execute `npm test` and verify all tests pass"

### 3. Include Context
```markdown
## Step 3: Update Database Schema
Run the migration to add the new user_preferences table:
```bash
npm run migrate
```

This adds columns for theme, language, and notification settings.
```

### 4. Handle Errors
```markdown
## Step 2: Build Application
```bash
npm run build
```

**If build fails:**
- Check for TypeScript errors
- Verify all dependencies installed
- Review build logs for specific errors
```

### 5. Provide Verification
```markdown
## Step 4: Deploy to Production
```bash
./deploy.sh production
```

**Verify deployment:**
- Check application is accessible
- Verify health check endpoint returns 200
- Monitor error logs for 5 minutes
```

## Testing Workflows

1. **Test each step**: Verify instructions are clear
2. **Test with real data**: Use actual project files
3. **Test error paths**: Verify error handling works
4. **Test auto-execution**: Ensure // turbo commands are safe
5. **Get user feedback**: Iterate based on actual usage
