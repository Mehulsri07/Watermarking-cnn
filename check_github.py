"""
Check what your actual GitHub repository name is
"""
import subprocess
import re

def check_github_repo():
    print("="*70)
    print("GITHUB REPOSITORY CHECKER")
    print("="*70)
    
    # Check git remote
    print("\n📍 Checking your git remote...")
    try:
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        output = result.stdout
        print(output)
        
        # Extract repo name from URL
        match = re.search(r'github\.com[:/]Mehulsri07/([^.\s]+)', output)
        if match:
            repo_name = match.group(1)
            print(f"\n✓ Found repository name: {repo_name}")
            
            # Check what the code expects
            print("\n" + "-"*70)
            print("COMPARISON")
            print("-"*70)
            print(f"Git remote points to:  {repo_name}")
            print(f"Code references:       Watermarking-cnn")
            
            if repo_name == "Watermarking-cnn":
                print("\n✅ MATCH! Everything is correct.")
                print("\nIf you're still getting errors in Colab:")
                print("1. Make sure the repository is PUBLIC")
                print("2. Wait a few minutes after pushing")
                print("3. Try clearing Colab cache")
                
            elif repo_name.lower() == "watermarking-cnn":
                print("\n⚠️  MISMATCH! Names don't match exactly.")
                print("\nYou have two options:")
                print("\nOption 1 (Recommended): Rename GitHub repo")
                print("  1. Go to: https://github.com/Mehulsri07/" + repo_name)
                print("  2. Settings → Repository name")
                print("  3. Change to: Watermarking-cnn")
                print("  4. Click Rename")
                print("  5. Run: git remote set-url origin https://github.com/Mehulsri07/Watermarking-cnn.git")
                
                print("\nOption 2: Update code to match GitHub")
                print("  Run: python fix_repo_name.py")
                
            else:
                print("\n❌ DIFFERENT! Repository names don't match.")
                print(f"\nYour GitHub repo: {repo_name}")
                print(f"Your code expects: Watermarking-cnn")
                print("\nRun: python fix_repo_name.py")
        else:
            print("\n⚠️  Could not extract repository name from remote URL")
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error running git command: {e}")
        print("\nMake sure you're in the watermark-cnn directory")
        return
    except FileNotFoundError:
        print("\n✗ Git is not installed or not in PATH")
        return
    
    # Check if repo is public
    print("\n" + "-"*70)
    print("CHECKLIST")
    print("-"*70)
    print("\n□ Repository is PUBLIC (required for Colab)")
    print("□ Repository name matches code references")
    print("□ Changes have been pushed to GitHub")
    print("□ Waited a few minutes after pushing")
    
    print("\n" + "="*70)
    print("To verify your repo is public:")
    print("1. Go to: https://github.com/Mehulsri07")
    print("2. Check if you can see the repository without logging in")
    print("3. If not, go to Settings → Danger Zone → Change visibility → Public")
    print("="*70)

if __name__ == "__main__":
    check_github_repo()
