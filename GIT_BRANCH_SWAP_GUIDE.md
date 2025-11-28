# Git Branch Swap Guide

Complete step-by-step instructions to swap branches and reorganize your repository.

## Goal
- Make the Python+SQLite MVP version the new `main` branch (default)
- Rename the current full-stack version to `fullstack` branch
- Delete the temporary `claude/python+sqlite-015FXiJYaX39SxRbP47USpTS` branch

---

## 📥 Step 1: Fetch the Branch from GitHub

```bash
# Navigate to your project folder
cd /path/to/student-management-API_c6e

# Fetch all remote branches
git fetch --all

# Verify you can see both branches
git branch -a
```

**Expected output:**
```
* main
  remotes/origin/main
  remotes/origin/claude/python+sqlite-015FXiJYaX39SxRbP47USpTS
```

---

## 🔄 Step 2: Rename Branches Locally (Swap them)

```bash
# 1. Make sure you're on main
git checkout main

# 2. Rename current main → fullstack (to preserve the full-stack version)
git branch -m main fullstack

# 3. Create a local branch from the claude/python+sqlite branch and name it 'main'
git checkout -b main origin/claude/python+sqlite-015FXiJYaX39SxRbP47USpTS

# 4. Verify your branches
git branch
```

**Expected output:**
```
  fullstack
* main
```

**Verification - Check what's on each branch:**
```bash
# Check main (should be MVP version)
git checkout main
ls -la
# Should see: student_manager.py, README_MVP.md

# Check fullstack (should be full-stack version)
git checkout fullstack
ls -la
# Should see: backend.py, index.html, app.js, style.css
```

---

## 🚀 Step 3: Push Changes to GitHub and Clean Up

```bash
# 1. Push the new 'main' branch (this will overwrite the old main on GitHub)
git checkout main
git push origin main --force

# 2. Push the 'fullstack' branch (this is the old main content)
git checkout fullstack
git push -u origin fullstack

# 3. Delete the claude/ branch from GitHub (no longer needed)
git push origin --delete claude/python+sqlite-015FXiJYaX39SxRbP47USpTS
```

**Expected output for step 3:**
```
To github.com:fp-bits/student-management-API_c6e.git
 - [deleted]         claude/python+sqlite-015FXiJYaX39SxRbP47USpTS
```

---

## 🌐 Step 4: Update Default Branch on GitHub (via GitHub UI)

After pushing, update GitHub's default branch:

1. Go to: `https://github.com/fp-bits/student-management-API_c6e/settings/branches`
2. Under "Default branch", click the **switch/edit** icon (⇄ or pencil icon)
3. Select `main` from the dropdown
4. Click **"Update"** and confirm the warning

**Note:** This step ensures when people clone your repo, they get the MVP version by default.

---

## ✅ Step 5: Final Verification

```bash
# Check local branches
git branch -vv

# Check remote branches
git branch -r

# Verify you're on main
git checkout main
cat README_MVP.md  # Should exist

# Check fullstack branch
git checkout fullstack
cat backend.py     # Should exist
```

**Expected remote branches:**
```
git branch -r
  origin/fullstack
  origin/main
```

---

## 📊 Final Result

After these steps, you'll have:

| Branch | Content | Location | Default |
|--------|---------|----------|---------|
| `main` | Python+SQLite MVP | GitHub + Local | ✅ Yes |
| `fullstack` | Full-stack Flask version | GitHub + Local | ❌ No |
| ~~`claude/python+sqlite-015FX...`~~ | Deleted | ❌ Removed | N/A |

---

## 🆘 Troubleshooting

### If force push fails:
```bash
# Make sure you're on the right branch
git branch

# Try force push with lease (safer)
git push origin main --force-with-lease
```

### If you need to undo everything:
```bash
# Reset to remote state
git fetch origin
git checkout main
git reset --hard origin/main

# Restore branch that was renamed
git branch -m fullstack main
```

### If you get "branch not found" errors:
```bash
# Verify remote branches exist
git ls-remote --heads origin

# Re-fetch everything
git fetch --all --prune
```

---

## 💡 Alternative Branch Names

If you prefer different names instead of `fullstack`, you can use:

```bash
# Instead of step 2 above, use:
git branch -m main flask-version
# or
git branch -m main web-version
# or
git branch -m main python-flask

# Then push with the new name:
git push -u origin flask-version
```

---

## 📝 Summary of Commands (Quick Copy)

```bash
# Step 1: Fetch
git fetch --all

# Step 2: Rename locally
git checkout main
git branch -m main fullstack
git checkout -b main origin/claude/python+sqlite-015FXiJYaX39SxRbP47USpTS

# Step 3: Push changes
git checkout main
git push origin main --force
git checkout fullstack
git push -u origin fullstack
git push origin --delete claude/python+sqlite-015FXiJYaX39SxRbP47USpTS

# Step 4: Update default branch via GitHub UI

# Step 5: Verify
git branch -r
git checkout main && ls -la
git checkout fullstack && ls -la
```

---

## ✨ Done!

Your repository is now reorganized with:
- **main** = Simple MVP version (default for new clones)
- **fullstack** = Complete web application version

Users can easily switch between versions:
```bash
git checkout main        # Python+SQLite MVP
git checkout fullstack   # Full-stack Flask app
```
