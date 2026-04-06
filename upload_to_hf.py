"""
Upload Smart Inbox Assistant to Hugging Face Hub
"""

from huggingface_hub import HfApi, login
import os

def upload_to_huggingface(repo_name="smart-inbox-rl", organization=None):
    """
    Upload the project to Hugging Face Hub as a Space
    
    Steps:
    1. Create HF account at https://huggingface.co
    2. Get token from Settings > Access Tokens
    3. Run this script
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
    
    # Create repo name with username or org
    if organization:
        repo_id = f"{organization}/{repo_name}"
    else:
        username = api.whoami()["name"]
        repo_id = f"{username}/{repo_name}"
    
    print(f"\n📦 Creating repository: {repo_id}\n")
    
    # Create repository
    api.create_repo(
        repo_id=repo_id,
        repo_type="space",
        space_sdk="gradio",
        exist_ok=True
    )
    
    print(f"✓ Repository created: https://huggingface.co/spaces/{repo_id}")
    print("✓ Files uploaded successfully!\n")
    
    return repo_id


if __name__ == "__main__":
    upload_to_huggingface()
