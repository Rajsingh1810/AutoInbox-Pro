"""
Complete upload script for AutoInbox Pro to Hugging Face Spaces
Uploads all necessary files automatically
"""

from huggingface_hub import HfApi
import os

def upload_all_files():
    """Upload all project files to HF Space"""
    
    api = HfApi()
    repo_id = "Raj-Heikens/AutoInbox-Pro"
    
    print("\n" + "="*60)
    print("🚀 Uploading to Hugging Face Spaces")
    print(f"Space: {repo_id}")
    print("="*60 + "\n")
    
    # Files to upload
    files = [
        "app.py",
        "email_env.py", 
        "requirements.txt",
    ]
    
    # Check for models
    if os.path.exists("./models/easy/final_model.zip"):
        print("📦 Found trained models - will upload...")
        files.extend([
            "models/easy/final_model.zip",
            "models/medium/final_model.zip", 
            "models/hard/final_model.zip"
        ])
    
    success_count = 0
    error_count = 0
    
    for file_path in files:
        try:
            if os.path.exists(file_path):
                print(f"⬆️  Uploading: {file_path}")
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=file_path,
                    repo_id=repo_id,
                    repo_type="space"
                )
                print(f"   ✅ Success")
                success_count += 1
            else:
                print(f"   ⚠️  Not found: {file_path}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            error_count += 1
    
    print("\n" + "="*60)
    print(f"📊 Upload Complete: {success_count} succeeded, {error_count} failed")
    print("="*60)
    
    if error_count == 0:
        print("\n✅ All files uploaded successfully!")
        print("\n⏱️  Your space will build in 2-5 minutes...")
        print(f"\n🔗 Visit: https://huggingface.co/spaces/{repo_id}")
        print("\n⚠️  IMPORTANT: Don't forget to add README.md!")
        print("   Copy the content from README_HF.md to README.md")
    else:
        print(f"\n⚠️  {error_count} file(s) failed to upload.")
        print("Check the errors above and try again.")
    
    return success_count, error_count

if __name__ == "__main__":
    upload_all_files()
