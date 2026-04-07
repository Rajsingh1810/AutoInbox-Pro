# 🎯 Deploy to Hugging Face - Step by Step

## 📍 Your Space URL
**https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro**

---

## 🚀 METHOD 1: Python Script (EASIEST - Recommended)

### Step 1: Install huggingface_hub
```bash
pip install huggingface_hub
```

### Step 2: Get Your Token
1. Open browser: **https://huggingface.co/settings/tokens**
2. Click **"New token"** button
3. Name it: `AutoInbox Deploy`
4. Type: Select **"Write"**
5. Click **"Generate a token"**
6. **COPY THE TOKEN** (it looks like: `hf_xxxxxxxxxxxxxxxx`)

### Step 3: Run Deploy Script
```bash
cd c:\Users\RAJ\Downloads\smart-inbox-rl
python upload_to_hf.py
```

### Step 4: Enter Token
When prompted: `Enter your Hugging Face token: `
Paste your token and press Enter

### Step 5: Wait for Upload
The script will upload files automatically. Wait for it to finish.

### Step 6: Wait for Build
Go to your space: https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
Wait **2-5 minutes** for it to build.

### ✅ Done! Your space is live!

---

## 🔧 METHOD 2: Manual Upload (No Scripts)

### Step 1: Go to Your Space
Open: https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro

### Step 2: Navigate to Files
Click the **"Files"** tab at the top

### Step 3: Add Files
Click **"Add file"** → **"Upload files"**

### Step 4: Upload These Files
Drag and drop or select:
1. ✅ `app.py`
2. ✅ `email_env.py`
3. ✅ `requirements.txt`

### Step 5: Create README.md
1. Click **"Add file"** → **"Create a new file"**
2. Name it: `README.md`
3. Copy content from `README_HF.md` (including the `---` YAML frontmatter)
4. Click **"Commit"**

### Step 6: Wait for Build
Wait **2-5 minutes**, then test your space!

---

## 🎨 What Your Space Will Look Like

After deployment, visitors will see:

```
┌─────────────────────────────────────────┐
│  📧 Smart Inbox Assistant               │
│                                         │
│  An AI-powered email classifier using   │
│  Reinforcement Learning!                │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │ 📧 Enter Email Text               │  │
│  │ [Paste any email here...]         │  │
│  │                                   │  │
│  │ 🎯 Difficulty Level               │  │
│  │ ○ Easy  ○ Medium  ○ Hard         │  │
│  │                                   │  │
│  │    [🔍 Classify Email]            │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │ 🤖 AI Decision                    │  │
│  │ ⭐ Action: Mark as Important      │  │
│  │                                   │  │
│  │ 📊 Mode: easy                     │  │
│  └───────────────────────────────────┘  │
│                                         │
│  💡 Try These Examples:                 │
│  [Example emails list]                  │
└─────────────────────────────────────────┘
```

---

## ⚠️ Important Notes

### File Structure on HF Spaces
Your space should have these files:
```
AutoInbox-Pro/
├── app.py                 ← Main Gradio app
├── email_env.py           ← RL environment
├── requirements.txt       ← Python dependencies
└── README.md              ← Space configuration (with YAML frontmatter)
```

### README.md Must Have YAML Frontmatter
The first lines MUST be:
```yaml
---
title: AutoInbox Pro - RL Email Classifier
emoji: 📧
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.47.1
app_file: app.py
python_version: 3.11.8
license: mit
short_description: AI-powered email classifier using Reinforcement Learning (PPO)
disable_embedding: true
---
```

### Models (Optional but Recommended)
If you have trained models:
```
models/
├── easy/final_model.zip
├── medium/final_model.zip
└── hard/final_model.zip
```

These will make your AI much more accurate!

---

## 🧪 Test Before Deploy (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

This opens http://localhost:7860 in your browser.
Test it works, then deploy!

---

## 🐛 Troubleshooting

### Space shows "Building" forever
- Click **"Build Logs"** tab
- Look for error messages
- Common fix: Click **"Settings"** → **"Factory reboot"**

### "Error importing module"
- Check all packages are in `requirements.txt`
- Look for typos in imports in `app.py`

### Space shows blank page
- Wait longer (can take 5+ minutes first time)
- Check browser console for errors (F12)
- Try "Reboot" in Settings

### Models not working
- Models must be uploaded with Git LFS
- Use Method 1 (Python script) for automatic handling

---

## 📞 Need More Help?

- **HF Spaces Docs**: https://huggingface.co/docs/hub/spaces
- **Gradio Docs**: https://www.gradio.app/docs/
- **Community**: https://discuss.huggingface.co/

---

## ✨ After Deployment

1. **Test** with these example emails:
   - Easy: "WIN MONEY NOW!!! Click here"
   - Medium: "Submit assignment before midnight"
   - Hard: "Can we meet tomorrow to discuss?"

2. **Share** your space:
   - Tweet about it
   - Share on LinkedIn
   - Add to your portfolio

3. **Improve** it:
   - Train with more data
   - Add more email types
   - Customize the UI

---

**Ready to deploy?** Run this now:
```bash
python upload_to_hf.py
```

🚀 Good luck!
