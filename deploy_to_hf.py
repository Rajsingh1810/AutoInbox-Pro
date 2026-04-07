"""
Quick deploy script for Hugging Face Spaces
Usage: python deploy_to_hf.py
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and report results"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    print(f"Running: {command}\n")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Success!")
        if result.stdout:
            print(result.stdout)
    else:
        print(f"❌ Failed!")
        if result.stderr:
            print(result.stderr)
    
    return result.returncode == 0

def main():
    print("\n🚀 Smart Inbox Assistant - HF Spaces Deployer")
    print("="*60)
    
    # Check if git is installed
    if not run_command("git --version", "Checking Git installation"):
        print("\n⚠️ Git is not installed. Please install Git first:")
        print("https://git-scm.com/downloads")
        return
    
    # Check if git-lfs is installed
    print("\n📦 Checking Git LFS...")
    result = subprocess.run("git lfs version", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("⚠️ Git LFS is not installed. Installing...")
        if not run_command("git lfs install", "Installing Git LFS"):
            print("\n⚠️ Failed to install Git LFS. Please install manually:")
            print("https://git-lfs.com/")
            return
    
    # Initialize git repo if not already done
    if not os.path.exists(".git"):
        run_command("git init", "Initializing Git repository")
        run_command('git lfs track "*.zip"', "Tracking model files with Git LFS")
        run_command('git lfs track "*.model"', "Tracking model files with Git LFS")
    
    # Add remote
    print("\n🔗 Setting up Hugging Face remote...")
    result = subprocess.run(
        "git remote -v",
        shell=True,
        capture_output=True,
        text=True
    )
    
    if "huggingface.co" not in result.stdout:
        run_command(
            "git remote add hf https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro",
            "Adding Hugging Face remote"
        )
    
    # Add all files
    run_command("git add .", "Adding all files")
    
    # Commit
    run_command('git commit -m "Deploy to Hugging Face Spaces"', "Committing changes")
    
    # Push
    print("\n🚀 Pushing to Hugging Face Spaces...")
    print("This may take a while due to model files...")
    success = run_command(
        "git push hf main",
        "Pushing to Hugging Face"
    )
    
    if success:
        print("\n" + "="*60)
        print("🎉 Deployment Successful!")
        print("="*60)
        print("\nYour space is now available at:")
        print("https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro")
        print("\n⏱️  It may take a few minutes to build...")
    else:
        print("\n" + "="*60)
        print("⚠️ Push failed. Try these alternatives:")
        print("="*60)
        print("\n1. Manual git push:")
        print("   git push hf main")
        print("\n2. Use huggingface_hub Python package:")
        print("   python upload_to_hf.py")
        print("\n3. Upload via web interface:")
        print("   https://huggingface.co/spaces/Raj-Heikens/AutoInbox-Pro")

if __name__ == "__main__":
    main()
