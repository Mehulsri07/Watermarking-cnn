# 📤 How to Update GitHub

Simple guide to push your changes to GitHub.

---

## 🚀 Quick Method (Easiest)

### Windows:
```bash
push_to_github.bat
```

### Linux/Mac:
```bash
chmod +x push_to_github.sh
./push_to_github.sh
```

That's it! The script will automatically:
1. Add all changes
2. Commit with a message
3. Push to GitHub

---

## 📝 Manual Method (Step by Step)

If you prefer to do it manually or want more control:

### Step 1: Check Status
```bash
git status
```
This shows what files have changed.

### Step 2: Add All Changes
```bash
git add .
```
This stages all changes for commit.

### Step 3: Commit Changes
```bash
git commit -m "Update: Fixed imports and Colab notebook"
```
You can change the message to describe your changes.

### Step 4: Push to GitHub
```bash
git push origin main
```

---

## 🔐 Authentication

If GitHub asks for credentials:

### Option 1: Personal Access Token (Recommended)
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Copy the token
5. Use token as password when pushing

### Option 2: GitHub CLI
```bash
# Install GitHub CLI first
gh auth login
```

### Option 3: SSH Keys
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub
# Copy the public key and add it to GitHub settings
```

---

## ✅ Verify Upload

After pushing, check:

1. **GitHub Repository:**
   https://github.com/Mehulsri07/Watermarking-cnn

2. **Colab Notebook:**
   https://colab.research.google.com/github/Mehulsri07/Watermarking-cnn/blob/main/watermark_colab.ipynb

3. **Files Updated:**
   - README.md
   - watermark_colab.ipynb
   - All Python scripts
   - New helper files

---

## 🐛 Troubleshooting

### "Permission denied"
- Use personal access token instead of password
- Or set up SSH keys

### "Repository not found"
- Check repository name: `Watermarking-cnn` (capital W)
- Make sure repository exists on GitHub
- Verify remote URL: `git remote -v`

### "Failed to push"
- Pull first: `git pull origin main`
- Then push: `git push origin main`

### "Merge conflict"
```bash
# Pull and merge
git pull origin main

# Fix conflicts in files
# Then commit and push
git add .
git commit -m "Resolved conflicts"
git push origin main
```

---

## 📊 What Gets Updated

When you push, these changes will be uploaded:

**Modified Files:**
- ✅ README.md (updated links)
- ✅ watermark_colab.ipynb (fixed clone URL)
- ✅ train_and_evaluate.py (added path fix)
- ✅ trainer.py (added path fix)
- ✅ evaluate_model.py (added path fix)
- ✅ embed_and_extract.py (added path fix)
- ✅ All __init__.py files (added content)

**New Files:**
- ✅ SETUP_COMPLETE.md
- ✅ check_references.py
- ✅ push_to_github.bat/sh
- ✅ HOW_TO_UPDATE_GITHUB.md

**Deleted Files:**
- ❌ QUICKSTART.md (merged into README)
- ❌ COLAB_INSTRUCTIONS.md (merged into notebook)
- ❌ READY_TO_UPLOAD.md (no longer needed)

---

## 🎯 After Pushing

1. **Test in Colab:**
   - Open the Colab link
   - Run all cells
   - Verify it works

2. **Update Repository Settings:**
   - Add description: "CNN-based invisible image watermarking using DWT"
   - Add topics: `deep-learning`, `watermarking`, `cnn`, `tensorflow`, `computer-vision`
   - Make sure it's PUBLIC

3. **Share:**
   - Share the Colab link with others
   - Add the badge to your profile
   - Star your own repo 😊

---

## 💡 Tips

### Commit Often
```bash
git add .
git commit -m "Descriptive message"
git push origin main
```

### Check Before Pushing
```bash
git status          # See what changed
git diff            # See exact changes
git log --oneline   # See commit history
```

### Undo Last Commit (if needed)
```bash
git reset --soft HEAD~1  # Undo commit, keep changes
git reset --hard HEAD~1  # Undo commit, discard changes
```

---

## 🆘 Need Help?

If you encounter issues:

1. Check error message carefully
2. Google the error message
3. Check GitHub status: https://www.githubstatus.com/
4. Ask on Stack Overflow
5. Open an issue on GitHub

---

**Ready to push?** Just run `push_to_github.bat` (Windows) or `./push_to_github.sh` (Linux/Mac)!
