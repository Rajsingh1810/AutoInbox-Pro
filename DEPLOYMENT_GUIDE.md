# Deploy to Hugging Face Spaces - Quick Guide

## Option 1: Using Git (Recommended)

### Step 1: Install Git LFS
Hugging Face Spaces requires Git LFS for model files.

```bash
git lfs install
```

### Step 2: Clone your HF Space
```bash
git clone https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
cd AutoInbox-Pro
```

### Step 3: Copy all files from this project
Copy these files to the cloned repository:
- `app.py`
- `email_env.py`
- `requirements.txt`
- `README_HF.md` (rename to `README.md`)

### Step 4: Add trained models (Optional but recommended)
```bash
# Create models directory
mkdir -p models/easy models/medium models/hard

# Copy your trained models
cp path/to/models/easy/final_model.zip models/easy/
cp path/to/models/medium/final_model.zip models/medium/
cp path/to/models/hard/final_model.zip models/hard/
```

### Step 5: Commit and push
```bash
git add .
git commit -m "Initial commit: Smart Inbox RL Assistant"
git push
```

## Option 2: Using Hugging Face Hub API

```python
from huggingface_hub import HfApi

api = HfApi()

# Upload all files
api.upload_folder(
    folder_path="c:/Users/RAJ/Downloads/smart-inbox-rl",
    repo_id="Raj-Heikens/AutoInbox-Pro",
    repo_type="space"
)
```

## Option 3: Manual Upload via Web Interface

1. Go to: https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
2. Click "Files" → "Add file" → "Upload files"
3. Upload:
   - `app.py`
   - `email_env.py`
   - `requirements.txt`
   - `README.md` (rename README_HF.md)
4. For models, use Git LFS (they're too large for web upload)

## Important Notes

### Git LFS is Required for Models
The trained model files (.zip) are large and MUST be tracked with Git LFS:

```bash
# Before committing models
git lfs track "*.zip"
git lfs track "*.model"
git add .gitattributes
```

### Space Configuration
The README_HF.md contains the space configuration:
- SDK: Gradio
- Python version: 3.11.8
- Theme: Green to Blue gradient

## Testing Locally First

Before deploying, test locally:
```bash
pip install -r requirements.txt
python app.py
```

## Troubleshooting

### Space won't start
- Check the logs in the HF Space interface
- Ensure all dependencies are in requirements.txt
- Verify README_HF.md has correct YAML headers

### Models not loading
- Ensure Git LFS is installed and tracking model files
- Check model paths in app.py
- Verify models are uploaded with `git lfs push`

### Import errors
- All required packages must be in requirements.txt
- HF Spaces installs from requirements.txt automatically

## Your Space URL
After deployment, your space will be available at:
https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
