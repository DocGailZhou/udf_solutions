
# GitHub CLI Merge Guide

A simple step-by-step guide for creating and merging pull requests using GitHub CLI.

## Prerequisites

Ensure you're authenticated with GitHub CLI:
```bash
gh auth login
```

## Quick Workflow: fabric_test → main

### Step 1: Create Pull Request
```bash
gh pr create --base main --head fabric_test --title "Merge fabric_test changes to main" --body "Merging fabric_test branch changes to main branch"
```

### Step 2: Merge Pull Request
```bash
gh pr merge 1 --squash
```

> **Note**: We use `--squash` without `--delete-branch` to preserve the fabric_test branch (synced to fabric workspace)

## Alternative Commands

### View PR before merging:
```bash
gh pr view 1
gh pr view --web 1  # Open in browser
```

### Check PR status:
```bash
gh pr status
gh pr list
```

### Different merge strategies:
```bash
gh pr merge 1 --merge     # Standard merge commit
gh pr merge 1 --squash    # Squash all commits into one
gh pr merge 1 --rebase    # Rebase and merge
```

## Complete Example

```bash
# 1. Authenticate (one-time setup)
gh auth login

# 2. Create PR
gh pr create --base main --head fabric_test --title "Your PR title" --body "Your PR description"

# 3. Review (optional)
gh pr view 1

# 4. Merge using squash
gh pr merge 1 --squash

# 5. Verify
gh pr list --state merged
```

## Tips

- PR numbers start from 1 and increment automatically
- Use `gh pr list` to see all PRs and their numbers
- The `fabric_test` branch remains active after merge
- Squash merge creates a cleaner commit history