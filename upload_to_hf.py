"""
Upload Smart Inbox Assistant to Hugging Face Hub Space
Updated for: https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
"""

from huggingface_hub import HfApi, login
import os

def upload_to_huggingface():
    """
    Upload the project to Hugging Face Hub as a Space
    Target: https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro
    """

    # Login to Hugging Face
    print("🔐 Login to Hugging Face:")
    print("   1. Go to https://huggingface.co/settings/tokens")
    print("   2. Create a new token (write access)")
    print()

    token = input("Enter your Hugging Face token: ").strip()
    login(token=token)

    # Initialize API
    api = HfApi()

    # Your space details
    repo_id = "Raj-Heikens/AutoInbox-Pro"

    print(f"\n📦 Uploading to: {repo_id}\n")

    # List files to upload
    files_to_upload = [
        "app.py",
        "email_env.py",
        "requirements.txt",
        "README_HF.md"
    ]
    
    # Check if models exist
    if os.path.exists("./models/easy/final_model.zip"):
        files_to_upload.extend([
            "models/easy/final_model.zip",
            "models/medium/final_model.zip",
            "models/hard/final_model.zip"
        ])
        print("📦 Including trained models...")

    # Upload each file
    for file_path in files_to_upload:
        if os.path.exists(file_path):
            print(f"⬆️  Uploading {file_path}...")
            try:
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=file_path,
                    repo_id=repo_id,
                    repo_type="space"
                )
                print(f"   ✅ {file_path} uploaded")
            except Exception as e:
                print(f"   ❌ Failed to upload {file_path}: {e}")
        else:
            print(f"   ⚠️  {file_path} not found, skipping")

    print(f"\n✓ Files uploaded to: https://huggingface.co/spaces/{repo_id}")
    print("\n⏱️  The space will automatically rebuild and deploy!")
    print("This may take 2-5 minutes...")

    return repo_id


if __name__ == "__main__":
    upload_to_huggingface()
