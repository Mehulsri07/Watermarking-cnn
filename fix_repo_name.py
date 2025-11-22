"""
Script to update repository name references
Use this if your GitHub repo has a different name than the code expects
"""
import os
import re

def update_references(old_name, new_name):
    """Update all references from old_name to new_name"""
    
    files_to_update = [
        'README.md',
        'watermark_colab.ipynb',
        'update_placeholders.py',
        'push_to_github.bat',
        'push_to_github.sh',
        'HOW_TO_UPDATE_GITHUB.md',
        'SETUP_COMPLETE.md',
    ]
    
    print("="*70)
    print("REPOSITORY NAME UPDATER")
    print("="*70)
    print(f"\nChanging references from: {old_name}")
    print(f"                      to: {new_name}")
    print("\n" + "-"*70)
    
    updated_count = 0
    
    for filename in files_to_update:
        if not os.path.exists(filename):
            continue
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Replace all occurrences
            content = content.replace(old_name, new_name)
            
            if content != original_content:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Updated: {filename}")
                updated_count += 1
            else:
                print(f"○ No changes: {filename}")
                
        except Exception as e:
            print(f"✗ Error updating {filename}: {e}")
    
    print("\n" + "="*70)
    print(f"Updated {updated_count} file(s)")
    print("="*70)
    
    return updated_count

def main():
    print("\n" + "="*70)
    print("GITHUB REPOSITORY NAME FIXER")
    print("="*70)
    print("\nThis script updates all repository name references in your code.")
    print("\nCurrent references point to: Watermarking-cnn")
    print("\n" + "-"*70)
    
    print("\nWhat is your ACTUAL GitHub repository name?")
    print("(Check at: https://github.com/Mehulsri07)")
    print("\nOptions:")
    print("  1. Watermarking-cnn  (capital W, no hyphen)")
    print("  2. watermark-cnn     (lowercase, with hyphen)")
    print("  3. Custom name")
    print("  4. Exit (I'll rename my GitHub repo instead)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n✓ Already correct! No changes needed.")
        print("\nIf you're still getting errors, your GitHub repo might be named differently.")
        print("Go to https://github.com/Mehulsri07 and check the exact name.")
        return
    
    elif choice == "2":
        old_name = "Watermarking-cnn"
        new_name = "watermark-cnn"
        
    elif choice == "3":
        new_name = input("\nEnter your exact GitHub repository name: ").strip()
        if not new_name:
            print("Error: Repository name cannot be empty")
            return
        old_name = "Watermarking-cnn"
        
    elif choice == "4":
        print("\n" + "="*70)
        print("RECOMMENDED: Rename your GitHub repository")
        print("="*70)
        print("\n1. Go to: https://github.com/Mehulsri07/[your-repo-name]")
        print("2. Click: Settings")
        print("3. Scroll to: Repository name")
        print("4. Change to: Watermarking-cnn")
        print("5. Click: Rename")
        print("\nThen update your local remote:")
        print("  git remote set-url origin https://github.com/Mehulsri07/Watermarking-cnn.git")
        return
    
    else:
        print("Invalid choice")
        return
    
    print("\n" + "="*70)
    print("UPDATING FILES")
    print("="*70)
    
    updated = update_references(old_name, new_name)
    
    if updated > 0:
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print("\n1. Update git remote:")
        print(f"   git remote set-url origin https://github.com/Mehulsri07/{new_name}.git")
        print("\n2. Push changes:")
        print("   git add .")
        print(f"   git commit -m 'Update repository name to {new_name}'")
        print("   git push origin main")
        print("\n3. Test in Colab:")
        print(f"   https://colab.research.google.com/github/Mehulsri07/{new_name}/blob/main/watermark_colab.ipynb")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
