# GitHub CLI Guide

A quick reference guide for common GitHub CLI (`gh`) tasks.

## Authentication
```bash
# Login to GitHub
gh auth login

# Check authentication status
gh auth status

# Logout
gh auth logout
```

## Repository Management
```bash
# Clone a repository
gh repo clone owner/repo-name

# Create a new repository
gh repo create repo-name --public
gh repo create repo-name --private

# View repository information
gh repo view
gh repo view owner/repo-name

# Fork a repository
gh repo fork owner/repo-name

# Delete a repository
gh repo delete owner/repo-name
```

## Pull Requests
```bash
# Create a pull request
gh pr create --title "PR Title" --body "PR description"
gh pr create --base main --head feature-branch

# List pull requests
gh pr list
gh pr list --state open
gh pr list --state closed

# View a pull request
gh pr view 123
gh pr view --web 123

# Checkout a pull request
gh pr checkout 123

# Merge a pull request
gh pr merge 123
gh pr merge 123 --squash
gh pr merge 123 --rebase

# Close a pull request
gh pr close 123

# Reopen a pull request
gh pr reopen 123

# Review a pull request
gh pr review 123 --approve
gh pr review 123 --request-changes --body "Please fix..."
gh pr review 123 --comment --body "Looks good!"
```

## Creating PRs and Merge Workflows

### Step-by-Step: Creating a PR from fabric_test to main
```bash
# 1. First, make sure you're on the source branch (fabric_test)
git checkout fabric_test

# 2. Push your changes to remote (if not already pushed)
git push origin fabric_test

# 3. Create the pull request
gh pr create --base main --head fabric_test --title "Merge fabric_test changes to main" --body "Description of changes"

# 4. Open the PR in browser for review
gh pr view --web

# 5. Check PR status
gh pr status
```

### Advanced PR Creation Options
```bash
# Create PR with more details
gh pr create \
  --base main \
  --head fabric_test \
  --title "Feature: Add UDF solutions for fabric workspace" \
  --body "## Changes
- Added new UDF implementations
- Updated documentation
- Fixed configuration issues

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [ ] Manual testing completed" \
  --assignee @me \
  --reviewer username1,username2 \
  --label "enhancement,ready-for-review"

# Create draft PR
gh pr create --draft --title "WIP: Fabric test implementation"

# Create PR and auto-merge when checks pass
gh pr create --title "Hotfix" --body "Emergency fix" && gh pr merge --auto --squash
```

### Merge Strategies
```bash
# 1. Merge commit (creates a merge commit)
gh pr merge 123 --merge

# 2. Squash and merge (squashes all commits into one)
gh pr merge 123 --squash --delete-branch

# 3. Rebase and merge (replays commits without merge commit)
gh pr merge 123 --rebase --delete-branch

# Merge with custom commit message
gh pr merge 123 --squash --subject "feat: merge fabric_test functionality" --body "Detailed description of the merge"
```

### Complete Workflow Example: fabric_test → main
```bash
# Prerequisites: Ensure branches are up to date
git checkout main
git pull origin main
git checkout fabric_test
git pull origin fabric_test

# Optional: Rebase fabric_test on latest main
git rebase main

# Push updated fabric_test
git push origin fabric_test --force-with-lease

# Create the PR
gh pr create \
  --base main \
  --head fabric_test \
  --title "Merge fabric_test: UDF solutions implementation" \
  --body "## Summary
This PR merges the fabric_test branch containing:
- UDF implementation for Fabric workspace
- Documentation updates
- Infrastructure configurations

## Review Checklist
- [ ] Code review completed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] No merge conflicts"

# Check PR details and CI status
gh pr view
gh pr checks

# After approval, merge with squash
gh pr merge --squash --delete-branch

# Verify the merge
git checkout main
git pull origin main
git log --oneline -5
```

### Handling Merge Conflicts
```bash
# If conflicts occur during PR creation or merge
gh pr view 123  # Check conflict details

# Resolve conflicts locally
git checkout fabric_test
git rebase main  # or git merge main
# Fix conflicts in your editor
git add .
git rebase --continue  # or git commit for merge
git push origin fabric_test --force-with-lease

# Alternative: Use GitHub's web interface
gh pr view --web 123  # Resolve conflicts in browser
```

### Post-Merge Cleanup
```bash
# After successful merge, clean up branches
git checkout main
git pull origin main
git branch -d fabric_test  # Delete local branch
git push origin --delete fabric_test  # Delete remote branch

# Optional: Create a new branch for next feature
git checkout -b fabric_test_v2
git push -u origin fabric_test_v2
```

## Issues
```bash
# Create an issue
gh issue create --title "Issue title" --body "Issue description"

# List issues
gh issue list
gh issue list --state open
gh issue list --assignee @me

# View an issue
gh issue view 123
gh issue view --web 123

# Close an issue
gh issue close 123

# Reopen an issue
gh issue reopen 123

# Comment on an issue
gh issue comment 123 --body "Comment text"
```

## Workflows (GitHub Actions)
```bash
# List workflows
gh workflow list

# View workflow runs
gh run list

# View a specific workflow run
gh run view 123456

# Re-run a workflow
gh run rerun 123456

# Download workflow artifacts
gh run download 123456
```

## Releases
```bash
# Create a release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"

# List releases
gh release list

# View a release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0

# Delete a release
gh release delete v1.0.0
```

## Gists
```bash
# Create a gist
gh gist create file.txt
gh gist create file.txt --public

# List gists
gh gist list

# View a gist
gh gist view gist-id

# Edit a gist
gh gist edit gist-id

# Clone a gist
gh gist clone gist-id
```

## Branches and Status
```bash
# Check repository status
gh status

# List branches
git branch -a  # (use git CLI for branches)

# Switch branches
git checkout branch-name  # (use git CLI)

# View commit history with GitHub context
gh pr list --search "author:@me"
```

## Useful Flags and Options
```bash
# Open in browser
--web

# Output as JSON
--json

# Specify repository
--repo owner/repo-name

# Help for any command
gh help
gh pr --help
gh issue create --help
```

## Examples for This Repository
```bash
# Create PR from fabric_test to main
gh pr create --base main --head fabric_test --title "Merge fabric_test to main"

# View this repository
gh repo view DocGailZhou/udf_solutions

# Check if there are any open PRs
gh pr list --repo DocGailZhou/udf_solutions

# Create an issue for this project
gh issue create --title "Documentation update needed" --body "Need to update UDF documentation"
```

## Pro Tips
- Use `gh alias` to create shortcuts for frequently used commands
- Combine with `jq` for JSON parsing: `gh pr list --json number,title | jq`
- Use `gh config` to set default preferences
- Most commands accept `--help` for detailed usage information