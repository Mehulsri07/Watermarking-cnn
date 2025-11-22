"""
Script to verify all GitHub references are correct
"""
import os
import re

def check_file(filepath, correct_repo="Watermarking-cnn", correct_user="Mehulsri07"):
    """Check if file has correct references"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for wrong repo names
        wrong_patterns = [
            r'watermark-cnn(?!/)',  # watermark-cnn not followed by /
            r'github\.com/[^/]+/watermark-cnn',  # in GitHub URLs
        ]
        
        for pattern in wrong_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                issues.append(f"Found 'watermark-cnn' (should be '{correct_repo}')")
                break
        
        # Check for correct references
        correct_count = content.count(correct_repo)
        
        return issues, correct_count
    except Exception as e:
        return [f"Error reading file: {e}"], 0

def main():
    print("="*70)
    print("GITHUB REFERENCE CHECKER")
    print("="*70)
    print("\nChecking all files for correct GitHub references...")
    print(f"Expected repo: Watermarking-cnn")
    print(f"Expected user: Mehulsri07")
    print("\n" + "-"*70)
    
    files_to_check = [
        'README.md',
        'watermark_colab.ipynb',
        'update_placeholders.py',
    ]
    
    all_good = True
    
    for filename in files_to_check:
        if os.path.exists(filename):
            print(f"\n📄 {filename}")
            issues, correct_count = check_file(filename)
            
            if issues:
                all_good = False
                for issue in issues:
                    print(f"  ✗ {issue}")
            else:
                print(f"  ✓ All references correct ({correct_count} found)")
        else:
            print(f"\n📄 {filename}")
            print(f"  ⚠️  File not found")
    
    print("\n" + "="*70)
    if all_good:
        print("✅ ALL FILES HAVE CORRECT REFERENCES!")
        print("\nYour repository is ready to use:")
        print("  Repository: https://github.com/Mehulsri07/Watermarking-cnn")
        print("  Colab: https://colab.research.google.com/github/Mehulsri07/Watermarking-cnn/blob/main/watermark_colab.ipynb")
    else:
        print("⚠️  SOME FILES NEED CORRECTION")
        print("\nPlease review the issues above.")
    print("="*70)

if __name__ == "__main__":
    main()
