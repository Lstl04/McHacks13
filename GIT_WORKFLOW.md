# Git Workflow Guide - McHacks13 Team

## Repository Structure

### Main Branches
- **`main`** - Production-ready code. Protected branch.
- **Feature branches** - Individual work branches

---

## 🚨 IMPORTANT: Change Default Branch on GitHub

**You need to change the default branch from `louis` to `main` on GitHub:**

1. Go to: https://github.com/Lstl04/McHacks13/settings/branches
2. Under "Default branch", click the switch icon
3. Select `main` as the new default branch
4. Confirm the change

After this, you can delete the `louis` branch if needed.

---

## Workflow for Team Members

### 1. Clone the Repository (First Time)
```bash
git clone https://github.com/Lstl04/McHacks13.git
cd McHacks13
```

### 2. Starting New Work
**Always create a feature branch from updated main:**

```bash
# Make sure you're on main
git checkout main

# Get latest changes
git pull origin main

# Create your feature branch (use descriptive names)
git checkout -b feature/your-feature-name
# or
git checkout -b yourname/feature-description
```

**Branch Naming Conventions:**
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `yourname/task-name` - Personal development branches

Examples:
- `feature/user-authentication`
- `fix/api-connection-error`
- `louis/database-setup`

### 3. Working on Your Branch

```bash
# Check which branch you're on
git branch

# Make your changes, then stage them
git add .

# Commit with a clear message
git commit -m "Description of what you did"

# Push to GitHub
git push origin your-branch-name
```

### 4. Keeping Your Branch Updated

**Before you start working each day:**
```bash
# Get latest changes from main
git checkout main
git pull origin main

# Switch back to your branch
git checkout your-branch-name

# Merge main into your branch
git merge main
```

### 5. Merging Your Work to Main

**Option A: Pull Request (Recommended for teams)**
1. Push your branch to GitHub
2. Go to GitHub and create a Pull Request
3. Have a teammate review your code
4. Merge the PR on GitHub
5. Delete the branch after merging

**Option B: Direct Merge (Quick fixes only)**
```bash
# Make sure your work is committed
git checkout main
git pull origin main
git merge your-branch-name
git push origin main

# Delete your feature branch
git branch -d your-branch-name
```

---

## Common Scenarios

### Scenario 1: You Need Someone Else's Changes
```bash
# If they're on a different branch
git checkout their-branch-name
git pull origin their-branch-name

# Or merge their branch into yours
git checkout your-branch
git merge their-branch-name
```

### Scenario 2: Merge Conflicts
```bash
# After git merge, if there are conflicts:
# 1. Open the conflicting files
# 2. Look for conflict markers: <<<<<<<, =======, >>>>>>>
# 3. Resolve conflicts manually
# 4. Stage the resolved files
git add .
git commit -m "Resolve merge conflicts"
```

### Scenario 3: You Made Changes on the Wrong Branch
```bash
# Save your changes without committing
git stash

# Switch to the correct branch
git checkout correct-branch-name

# Apply your saved changes
git stash pop
```

### Scenario 4: Undo Last Commit (Not Pushed Yet)
```bash
# Keep changes but undo commit
git reset --soft HEAD~1

# Undo commit and changes (DANGEROUS!)
git reset --hard HEAD~1
```

---

## Team Best Practices

### ✅ DO:
- **Pull often** - Get latest changes multiple times per day
- **Commit often** - Small, focused commits are better
- **Write clear commit messages** - "Fix login bug" not "updates"
- **Create feature branches** - Don't work directly on main
- **Communicate** - Let team know what you're working on
- **Review code** - Check each other's PRs before merging

### ❌ DON'T:
- **Don't force push** - Avoid `git push --force` unless you know what you're doing
- **Don't commit secrets** - API keys, passwords should be in `.env` (already in `.gitignore`)
- **Don't commit dependencies** - `node_modules/`, `__pycache__/`, etc. are in `.gitignore`
- **Don't merge without testing** - Test your code before merging to main
- **Don't leave branches open** - Delete feature branches after merging

---

## Current Project Structure

```
McHacks13/
├── backend/           # Python/FastAPI backend
│   └── main.py
├── frontend/          # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── requirements.txt   # Python dependencies
└── .gitignore        # Ignored files
```

---

## Quick Reference

```bash
# Status of your files
git status

# See your branches
git branch

# See all branches including remote
git branch -a

# Switch branches
git checkout branch-name

# Create and switch to new branch
git checkout -b new-branch-name

# See commit history
git log --oneline

# See who changed what
git blame filename

# Discard changes to a file
git restore filename

# Update your local branch list
git fetch --prune
```

---

## Need Help?

- **Check status**: `git status`
- **Ask the team** in your group chat
- **GitHub Desktop**: If you prefer a GUI, use [GitHub Desktop](https://desktop.github.com/)

---

## Emergency: "I messed up!"

```bash
# See what branch you're on and what's changed
git status

# If you haven't pushed yet, you can usually undo
git log --oneline  # Find the commit you want to go back to
git reset --soft COMMIT_HASH

# If you pushed and need help - STOP and ask the team!
```

Remember: Git is designed to make it hard to permanently lose work. When in doubt, ask!
