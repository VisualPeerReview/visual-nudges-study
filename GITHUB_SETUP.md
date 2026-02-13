# GitHub Setup Guide

This guide will walk you through setting up this project on GitHub.

## Step 1: Create a GitHub Repository

### Via GitHub Website

1. Go to [github.com](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Fill in the details:
   - **Repository name**: `visual-nudges-study` (or your preferred name)
   - **Description**: "Analysis pipeline for Visual Nudges in Peer Review study"
   - **Visibility**: Choose Public or Private
   - **DON'T** initialize with README, .gitignore, or license (we already have these)
4. Click **Create repository**

### Via GitHub CLI (Alternative)

```bash
gh repo create visual-nudges-study --public --description "Analysis pipeline for Visual Nudges in Peer Review study"
```

## Step 2: Initialize Local Repository

Open your terminal and navigate to your project directory:

```bash
# Navigate to where you want your project
cd ~/projects  # or your preferred location

# Create project directory
mkdir visual-nudges-study
cd visual-nudges-study

# Copy all files from the outputs folder to here
# (You should have: Python scripts, README, requirements.txt, etc.)

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: R to Python conversion"
```

## Step 3: Connect to GitHub

Replace `yourusername` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/yourusername/visual-nudges-study.git

# Verify the remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### If Using SSH Instead of HTTPS

```bash
git remote add origin git@github.com:yourusername/visual-nudges-study.git
git push -u origin main
```

## Step 4: Set Up Branch Protection (Optional but Recommended)

On GitHub.com:

1. Go to your repository
2. Click **Settings** → **Branches**
3. Click **Add branch protection rule**
4. Branch name pattern: `main`
5. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
6. Click **Create**

## Step 5: Enable GitHub Actions

The repository includes a CI workflow that will:
- Test code on multiple Python versions
- Run linting checks
- Verify project structure

To enable:
1. GitHub Actions should be automatically enabled
2. Go to **Actions** tab to see workflow runs
3. On first push, the CI workflow will run automatically

## Step 6: Update Repository Settings

### Add Topics (Tags)

On the main repository page:
1. Click the gear icon ⚙️ next to "About"
2. Add topics: `python`, `data-analysis`, `peer-review`, `statistics`, `research`
3. Save changes

### Update README Links

Edit the README.md file and replace:
- `yourusername` with your GitHub username
- `[Your Name]` with your actual name
- `[your email]` with your contact email

```bash
# Edit the README
nano README.md  # or use your preferred editor

# Commit the changes
git add README.md
git commit -m "Update README with personal information"
git push
```

## Step 7: Create Releases (Optional)

### Tag Version 1.0.0

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Initial release: R to Python conversion"
git push origin v1.0.0
```

### Create Release on GitHub

1. Go to your repository on GitHub
2. Click **Releases** → **Draft a new release**
3. Tag version: `v1.0.0`
4. Release title: `v1.0.0 - Initial Release`
5. Description:
```markdown
## Initial Release

This is the first release of the Visual Nudges analysis pipeline in Python.

### Features
- Data cleaning and validation
- Descriptive statistics generation
- Comprehensive statistical analysis including:
  - Effect sizes (Hedges' g)
  - Bootstrap confidence intervals
  - Nonparametric sensitivity checks
  - Logistic regression for binary outcomes

### Installation
See [README.md](README.md) for installation instructions.

### What's Next
- Sample data examples
- Jupyter notebook tutorials
- Additional visualization tools
```
6. Click **Publish release**

## Step 8: Add Collaborators (If Applicable)

1. Go to **Settings** → **Collaborators**
2. Click **Add people**
3. Enter GitHub usernames
4. Choose permission level (Write, Maintain, or Admin)

## Step 9: Set Up GitHub Pages (Optional - for documentation)

If you want to host documentation:

1. Go to **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` → `/docs` (if you create a docs folder)
4. Click **Save**

## Step 10: Clone and Test

Test that everything works:

```bash
# Clone to a new location to test
cd ~/Desktop
git clone https://github.com/yourusername/visual-nudges-study.git
cd visual-nudges-study

# Set up and test
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python setup_project.py

# Verify
ls -la data/
ls -la results/
```

## Common Git Commands for Daily Use

```bash
# Check status
git status

# Create a new branch
git checkout -b feature/new-analysis

# Stage changes
git add filename.py
# or all files
git add .

# Commit changes
git commit -m "Add new feature"

# Push to GitHub
git push origin feature/new-analysis

# Update from GitHub
git pull origin main

# Switch branches
git checkout main

# Merge branch
git merge feature/new-analysis

# View commit history
git log --oneline
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:

**For HTTPS:**
```bash
# Set up credential helper
git config --global credential.helper cache
```

**For SSH:**
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

### Large Files

If you have large data files:
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.xlsx"
git lfs track "data/raw/*.csv"

# Commit the .gitattributes file
git add .gitattributes
git commit -m "Configure Git LFS"
```

### Undo Last Commit (Not Pushed)

```bash
git reset --soft HEAD~1
```

### Undo Changes to a File

```bash
git checkout -- filename.py
```

## Next Steps

1. ✅ Repository created and pushed
2. 📝 Update README with your information  
3. 🏷️ Add topics/tags to repository
4. 🚀 Create first release
5. 📄 Add sample data (if possible)
6. 📖 Write additional documentation
7. 🧪 Add more tests
8. 📊 Create example notebooks

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Markdown Guide](https://www.markdownguide.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Getting Help

If you encounter issues:
1. Check the [GitHub Community](https://github.community/)
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/git)
3. Review [Git documentation](https://git-scm.com/doc)

Happy coding! 🎉
