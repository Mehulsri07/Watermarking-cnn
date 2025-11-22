"""
Script to update all placeholder information with your actual details
"""
import os
import re

def update_file(filepath, replacements):
    """Update placeholders in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"  ✗ Error updating {filepath}: {e}")
        return False

def main():
    print("="*70)
    print("PLACEHOLDER UPDATE SCRIPT")
    print("="*70)
    print("\nThis script will replace placeholder information with your details.\n")
    
    # Get user information
    print("Please enter your information:")
    print("-"*70)
    
    github_username = input("GitHub Username: ").strip()
    if not github_username:
        print("Error: GitHub username is required!")
        return
    
    full_name = input("Full Name (optional, press Enter to skip): ").strip()
    email = input("Email (optional, press Enter to skip): ").strip()
    
    print("\n" + "="*70)
    print("UPDATING FILES")
    print("="*70)
    
    # Define replacements
    replacements = {
        'YOUR_USERNAME': github_username,
        'Mehulsri07': github_username,  # Replace existing username
    }
    
    if full_name:
        replacements['Your Name'] = full_name
        replacements['Mehul Srivastava'] = full_name
    
    if email:
        replacements['your.email@example.com'] = email
        replacements['meulsri.0701@gmail.com'] = email
    
    # Files to update
    files_to_update = [
        'README.md',
        'watermark_colab.ipynb',
        'QUICKSTART.md',
        'COLAB_INSTRUCTIONS.md',
        'LICENSE',
    ]
    
    updated_count = 0
    
    for filename in files_to_update:
        if os.path.exists(filename):
            print(f"\nUpdating {filename}...", end=" ")
            if update_file(filename, replacements):
                print("✓ Updated")
                updated_count += 1
            else:
                print("○ No changes needed")
        else:
            print(f"\n  ⚠️  {filename} not found, skipping...")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\n✓ Updated {updated_count} file(s)")
    print(f"\nReplacements made:")
    for old, new in replacements.items():
        print(f"  {old} → {new}")
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. Review the updated files")
    print("2. Upload to GitHub:")
    print(f"   git remote add origin https://github.com/{github_username}/watermark-cnn.git")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git push -u origin main")
    print("\n3. Open in Colab:")
    print(f"   https://colab.research.google.com/github/{github_username}/watermark-cnn/blob/main/watermark_colab.ipynb")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
