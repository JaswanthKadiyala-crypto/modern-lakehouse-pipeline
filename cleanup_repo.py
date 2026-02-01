"""
Git Repo Cleanup Script
Removes unnecessary files and organizes the repository
"""

import os
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a git command and log output"""
    print(f"\n{'='*60}")
    print(f"✓ {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.returncode != 0 and result.stderr:
            print(f"Warning: {result.stderr}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def cleanup_git_repo():
    """Clean up Git repository"""
    
    print("\n" + "="*60)
    print("GIT REPOSITORY CLEANUP")
    print("="*60)
    
    # Change to repo directory
    repo_path = r"c:\Users\jkadi\Documents\modern-lakehouse-pipeline"
    os.chdir(repo_path)
    
    # 1. Check Git status
    run_command(
        "git status",
        "Checking current Git status"
    )
    
    # 2. Remove untracked files (dry run first)
    print("\n" + "-"*60)
    print("Untracked files that will be removed:")
    print("-"*60)
    run_command(
        "git clean -fd --dry-run",
        "Showing files to be removed"
    )
    
    # 3. Show what will be removed
    print("\nRemove these untracked files? (y/n)")
    response = input()
    
    if response.lower() == 'y':
        run_command(
            "git clean -fd",
            "Removing untracked files"
        )
    
    # 4. Remove Git cache and re-add with gitignore
    print("\n" + "-"*60)
    print("Refreshing Git index with .gitignore")
    print("-"*60)
    
    run_command(
        "git rm -r --cached .",
        "Clearing Git cache"
    )
    
    run_command(
        "git add .",
        "Re-adding files (respecting .gitignore)"
    )
    
    # 5. Show status before commit
    run_command(
        "git status",
        "Showing status after cleanup"
    )
    
    # 6. Commit cleanup
    print("\n" + "-"*60)
    print("Ready to commit cleanup? (y/n)")
    print("-"*60)
    response = input()
    
    if response.lower() == 'y':
        run_command(
            'git commit -m "chore: Clean up repo - remove untracked files and update gitignore"',
            "Committing cleanup"
        )
        
        # 7. Push to GitHub
        print("\nPush to GitHub? (y/n)")
        response = input()
        
        if response.lower() == 'y':
            run_command(
                "git push origin main",
                "Pushing to GitHub main branch"
            )
    
    # 8. Show final stats
    print("\n" + "="*60)
    print("CLEANUP COMPLETE")
    print("="*60)
    run_command(
        "git log --oneline -5",
        "Recent commits"
    )
    
    run_command(
        "git branch -a",
        "Available branches"
    )
    
    print("\n✓ Repository is clean and organized!")

if __name__ == '__main__':
    cleanup_git_repo()
