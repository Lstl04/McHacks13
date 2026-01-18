# Git Workflow Guide - McHacks13 Team

## Repository Structure

### Main Branch
- **`main`** - Default branch. All code merges here. ✅ **Now configured as default!**

---

## Workflow for Team Members (3 People)

### 1. Clone the Repository (First Time Only)
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
git checkout -b yourname/feature-description
```

**Branch Naming Conventions:**
- `yourname/feature-name` - Personal development branches
- `feature/feature-name` - Shared features
- `fix/bug-description` - Bug fixes

**Examples:**
- `louis/database-setup`
- `john/user-authentication`
- `sarah/frontend-components`

### 3. Working on Your Branch

```bash
# Check which branch you're on
git status

# Make your changes, then stage them
git add .

# Commit with a clear message
git commit -m "Add feature X" 

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

# Merge main into your branch to stay updated
git merge main
```

### 5. Merging Your Work to Main

**Option A: Pull Request on GitHub (Recommended)**
1. Push your branch: `git push origin your-branch-name`
2. Go to https://github.com/Lstl04/McHacks13
3. Click "Compare & pull request"
4. Add description of your changes
5. Have a teammate review
6. Click "Merge pull request"
7. Delete the branch after merging

**Option B: Direct Merge (For small changes)**
```bash
# Switch to main
git checkout main
git pull origin main

# Merge your branch
git merge your-branch-name

# Push to GitHub
git push origin main

# Delete your feature branch
git branch -d your-branch-name
```

---

## Common Scenarios

### Scenario 1: See What Changed
```bash
# See status of your files
git status

# See what changed in files
git diff

# See commit history
git log --oneline
```

### Scenario 2: You Need Someone Else's Work
```bash
# Pull their branch
git checkout their-branch-name
git pull origin their-branch-name

# Or merge their branch into yours
git checkout your-branch
git merge their-branch-name
```

### Scenario 3: Merge Conflicts
When two people edit the same file:
```bash
# After git merge, if there are conflicts:
# 1. Git will tell you which files have conflicts
# 2. Open those files and look for:
#    <<<<<<< HEAD
#    Your changes
#    =======
#    Their changes
#    >>>>>>> branch-name
# 3. Edit to keep what you want, delete the markers
# 4. Save the file
git add .
git commit -m "Resolve merge conflicts"
```

### Scenario 4: Made Changes on Wrong Branch
```bash
# Save your changes
git stash

# Switch to correct branch
git checkout correct-branch-name

# Apply your changes
git stash pop
```

### Scenario 5: Undo Last Commit (Not Pushed Yet)
```bash
# Keep changes, undo commit
git reset --soft HEAD~1

# Undo everything (BE CAREFUL!)
git reset --hard HEAD~1
```

---

## Team Best Practices

### ✅ DO:
- **Pull from main daily** - Stay synced with team
- **Commit often** - Small commits are better than huge ones
- **Write clear messages** - "Add login validation" not "changes"
- **Test before merging** - Make sure it works!
- **Communicate** - Tell team what you're working on
- **Delete old branches** - Keep repo clean

### ❌ DON'T:
- **Don't force push** - You'll overwrite others' work
- **Don't commit secrets** - API keys go in `.env` (already ignored)
- **Don't commit `node_modules/`** - Already in `.gitignore`
- **Don't work on main directly** - Always use feature branches
- **Don't leave conflicts unresolved** - Fix them immediately

---

## Current Project Structure

```
McHacks13/
├── backend/              # Python FastAPI backend
│   ├── main.py          # API endpoints
│   └── mchacks/         # Virtual environment
├── frontend/            # React + Vite frontend
│   ├── src/            # React components
│   ├── public/         # Static files
│   └── package.json    # Dependencies
├── requirements.txt    # Python dependencies
├── .gitignore         # Files Git ignores
└── GIT_WORKFLOW.md    # This file!
```

---

## Quick Reference Commands

```bash
# Check what branch you're on
git branch

# See all branches (local + remote)
git branch -a

# Create new branch
git checkout -b new-branch-name

# Switch branches
git checkout branch-name

# Update from GitHub
git pull

# See what changed
git status
git diff

# Stage all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin branch-name

# Get latest main
git checkout main && git pull origin main

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name
```

---

## Emergency: "I Messed Up!"

### If you haven't pushed yet:
```bash
# See where you are
git status
git log --oneline

# Go back to last commit (keeps changes)
git reset --soft HEAD~1

# Go back and DELETE changes (careful!)
git reset --hard HEAD~1
```

### If you already pushed:
**STOP! Ask your teammates before doing anything!**

Git makes it hard to lose work permanently. When in doubt:
1. Don't panic
2. Run `git status` and screenshot it
3. Ask the team for help

---

## Tips for Success

1. **Pull before you push** - Always `git pull` before `git push`
2. **Read the messages** - Git tells you what went wrong
3. **One feature per branch** - Don't mix unrelated changes
4. **Sync often** - Don't go days without pulling from main
5. **Use GitHub Desktop** - If command line is confusing: https://desktop.github.com/

---

## Need Help?

- **GitHub Repository**: https://github.com/Lstl04/McHacks13
- **Ask the team** in your group chat
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf

Remember: Everyone makes Git mistakes. The key is communicating with your team! 🚀
