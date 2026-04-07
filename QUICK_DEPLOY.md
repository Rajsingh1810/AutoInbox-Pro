# 🚀 Quick Deploy to Hugging Face Spaces

Your Space URL: **https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro**

## 📋 What's Been Prepared

✅ `app.py` - Updated for HF Spaces compatibility  
✅ `email_env.py` - RL Environment (ready)  
✅ `requirements.txt` - Optimized dependencies  
✅ `README_HF.md` - Space configuration file  
✅ `upload_to_hf.py` - Automated upload script  
✅ `deploy_to_hf.py` - Git-based deployment script  

## 🎯 Choose Your Deployment Method

### Method 1: Python Script (Easiest) ⭐ RECOMMENDED

```bash
# Step 1: Install huggingface_hub if not already installed
pip install huggingface_hub

# Step 2: Run the upload script
python upload_to_hf.py
```

This will:
- Prompt for your HF token (get one at: https://huggingface.co/settings/tokens)
- Upload all necessary files automatically
- Include trained models if they exist

### Method 2: Git Command Line

```bash
# Step 1: Navigate to project directory
cd c:\Users\RAJ\Downloads\smart-inbox-rl

# Step 2: Initialize git if not done
git init
git lfs install

# Step 3: Track model files
git lfs track "*.zip"

# Step 4: Add all files
git add .
git commit -m "Deploy to HF Spaces"

# Step 5: Add remote and push
git remote add hf https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
git push hf main
```

### Method 3: Manual Upload via Web

1. Go to: https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
2. Click **"Files"** → **"Add file"** → **"Upload files"**
3. Upload these files:
   - ✅ `app.py`
   - ✅ `email_env.py`
   - ✅ `requirements.txt`
   - ✅ `README_HF.md` (rename to `README.md` when uploading)

**Note**: For trained models, use Method 1 or 2 (Git LFS required for large files)

## ⚙️ Space Configuration

The `README_HF.md` file contains these settings:
- **SDK**: Gradio
- **Python Version**: 3.11.8
- **Theme**: Green → Blue gradient
- **Description**: AI-powered email classifier using Reinforcement Learning (PPO)

## 🔍 After Deployment

1. **Wait 2-5 minutes** for the space to build
2. Visit: https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
3. Check **Build Logs** if there are any issues
4. Test the app with sample emails

## 🧪 Test Locally First (Recommended)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app locally
python app.py
```

This opens a local Gradio interface at `http://localhost:7860`

## 📦 Including Trained Models

If you have trained models in `./models/`, they will be automatically included.

To train models first:
```bash
python train.py
```

This creates models in:
- `models/easy/final_model.zip`
- `models/medium/final_model.zip`
- `models/hard/final_model.zip`

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Space stuck building | Check "Build Logs" tab |
| Import errors | Verify all packages in requirements.txt |
| Models not loading | Ensure Git LFS is tracking .zip files |
| Gradio error | Check gradio version compatibility |

## 📞 Need Help?

- HF Spaces Docs: https://huggingface.co/docs/hub/spaces
- Gradio Docs: https://www.gradio.app/docs

---

**Ready to deploy?** Run: `python upload_to_hf.py` 🚀
