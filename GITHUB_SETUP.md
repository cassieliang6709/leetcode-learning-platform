# 🚀 GitHub Repository Setup Guide

Complete guide to set up your GitHub repository for this project.

## 📋 Pre-Setup Checklist

- ✅ Git repository initialized locally
- ✅ Initial commit created
- ✅ .gitignore configured
- ✅ README.md created
- ✅ LICENSE added

## 🌟 Step 1: Create GitHub Repository

### Option A: Via GitHub Website (Recommended)

1. **Go to GitHub**
   - Visit https://github.com
   - Log in to your account

2. **Create New Repository**
   - Click the `+` icon in the top right
   - Select "New repository"

3. **Repository Settings**
   ```
   Repository name: leetcode-learning-platform
   Description: AI-powered algorithm learning platform with personalized hints and code review
   Visibility: Public (or Private if you prefer)
   
   ❌ DO NOT initialize with:
      - README (we already have one)
      - .gitignore (we already have one)
      - License (we already have one)
   ```

4. **Click "Create repository"**

### Option B: Via GitHub CLI

```bash
# Install GitHub CLI if not installed
brew install gh

# Login to GitHub
gh auth login

# Create repository
gh repo create leetcode-learning-platform --public --source=. --remote=origin

# Push code
git push -u origin main
```

## 🔗 Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, you'll see instructions. Here's what to do:

```bash
cd /Users/liangyue/Documents/school/cs5001_project

# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/leetcode-learning-platform.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

## 📝 Step 3: Complete README.md

Update the following sections in `README.md`:

```markdown
## 👥 Authors

- Your Name (@YOUR_GITHUB_USERNAME) - Initial work

## 🚀 Quick Start

git clone https://github.com/YOUR_USERNAME/leetcode-learning-platform.git
```

Commit the changes:
```bash
git add README.md
git commit -m "docs: update README with GitHub info"
git push
```

## 🏷️ Step 4: Add Topics (Tags)

On your GitHub repository page:

1. Click "⚙️ Settings" (or find the "About" section on the right)
2. Click "⚙️" next to "About"
3. Add topics:
   - `leetcode`
   - `learning-platform`
   - `fastapi`
   - `react`
   - `postgresql`
   - `ai-powered`
   - `algorithm-learning`
   - `education`
   - `python`
   - `javascript`

## 📋 Step 5: Create GitHub Issues (Optional)

Create issues for future improvements:

### Issue 1: Integrate OpenAI API
```markdown
**Title:** Integrate Real OpenAI API for AI Features

**Description:**
Currently using simulated AI responses. Need to integrate actual OpenAI API for:
- Learning plan generation
- Code analysis
- Hint generation

**Labels:** enhancement, ai
```

### Issue 2: Add User Authentication
```markdown
**Title:** Implement User Authentication System

**Description:**
Add user registration, login, and session management.

**Labels:** enhancement, security
```

### Issue 3: Expand Problem Library
```markdown
**Title:** Import Full LeetCode Hot 100 Problems

**Description:**
Currently using demo problems. Import complete LeetCode Hot 100 dataset.

**Labels:** enhancement, content
```

## 🎯 Step 6: Set Up Branch Protection (Optional)

For collaborative work:

1. Go to repository Settings
2. Click "Branches" in left sidebar
3. Add rule for `main` branch:
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass
   - ✅ Require conversation resolution before merging

## 📊 Step 7: Add Repository Sections

### Description
```
AI-powered algorithm learning platform with personalized learning paths, intelligent multi-level hints, and automated code review. Built with FastAPI, React, and PostgreSQL.
```

### Website (if deployed)
```
https://your-app-url.com
```

### Topics (already added in Step 4)

## 🚀 Step 8: Create Releases

When ready to create a release:

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release v1.0.0 - Initial public release"
git push origin v1.0.0
```

Then on GitHub:
1. Go to "Releases"
2. Click "Create a new release"
3. Select tag: v1.0.0
4. Title: "v1.0.0 - Initial Release"
5. Description: List features and changes
6. Click "Publish release"

## 📄 Step 9: Add GitHub Actions (Optional)

Create `.github/workflows/ci.yml` for automated testing:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run linter
        run: |
          cd backend
          pip install flake8
          flake8 . --count --max-line-length=120

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      - name: Run linter
        run: |
          cd frontend
          npm run lint
```

## 🔒 Step 10: Secure Sensitive Information

**IMPORTANT:** Make sure these are in `.gitignore`:

- ✅ `.env` files
- ✅ `venv/` directory
- ✅ `node_modules/` directory
- ✅ Database files
- ✅ API keys

If you accidentally committed sensitive data:
```bash
# Remove from history (use with caution!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (dangerous - coordinate with team first)
git push origin --force --all
```

## 📱 Step 11: Update Social Preview

1. Create a project logo/banner (1280x640px)
2. Go to repository Settings
3. Scroll to "Social preview"
4. Upload image

## ✅ Verification Checklist

After setup, verify:

- [ ] Repository is accessible on GitHub
- [ ] README displays correctly
- [ ] All files are committed and pushed
- [ ] .gitignore is working (no venv/, node_modules/, .env)
- [ ] License is visible
- [ ] Topics/tags are added
- [ ] Description is set
- [ ] Clone URL works
- [ ] Issues can be created (if public)

## 🎉 You're Done!

Your repository is now set up! Share it:

```
Repository URL: https://github.com/YOUR_USERNAME/leetcode-learning-platform
Clone command: git clone https://github.com/YOUR_USERNAME/leetcode-learning-platform.git
```

## 📚 Next Steps

1. **Add Contributors**
   - Settings → Collaborators → Add people

2. **Enable Discussions** (optional)
   - Settings → Features → Discussions

3. **Add Project Board** (optional)
   - Projects → New project → Track tasks

4. **Set up GitHub Pages** (optional)
   - Deploy documentation or demo site

5. **Connect to Project Management**
   - Link to Jira, Trello, etc.

## 🆘 Troubleshooting

### "Repository already exists"
- Choose a different name or delete the existing repository

### "Permission denied (publickey)"
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/leetcode-learning-platform.git
```

### "Failed to push"
```bash
# Pull first if repository has content
git pull origin main --allow-unrelated-histories
git push -u origin main
```

---

**Need help?** Open an issue on GitHub or check the [documentation](README.md).

