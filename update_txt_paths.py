#!/usr/bin/env python3
"""Update all .txt file references in Python scripts to point to txt/ directory."""

import os
import re
import glob

def update_file_paths(filepath):
    """Update txt file paths in a Python file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Pattern 1: open('filename.txt')
    content = re.sub(
        r"open\('([^'/]+\.txt)'",
        r"open('txt/\1'",
        content
    )
    
    # Pattern 2: open("filename.txt")
    content = re.sub(
        r'open\("([^"/]+\.txt)"',
        r'open("txt/\1"',
        content
    )
    
    # Pattern 3: read_file('filename.txt')
    content = re.sub(
        r"read_file\('([^'/]+\.txt)'",
        r"read_file('txt/\1'",
        content
    )
    
    # Pattern 4: read_file("filename.txt")
    content = re.sub(
        r'read_file\("([^"/]+\.txt)"',
        r'read_file("txt/\1"',
        content
    )
    
    # Pattern 5: with open filename.txt patterns
    content = re.sub(
        r"with open\('([^'/]+\.txt)'",
        r"with open('txt/\1'",
        content
    )
    
    content = re.sub(
        r'with open\("([^"/]+\.txt)"',
        r'with open("txt/\1"',
        content
    )
    
    # Fix any double txt/txt/ patterns
    content = content.replace('txt/txt/', 'txt/')
    
    # Only write if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Find all Python files in current directory (not subdirectories)
python_files = glob.glob('*.py')

print("Updating txt file paths in Python scripts...")
print("=" * 60)

updated_count = 0
for pyfile in sorted(python_files):
    if pyfile == 'update_txt_paths.py':  # Skip this script
        continue
    
    if update_file_paths(pyfile):
        print(f"✓ Updated: {pyfile}")
        updated_count += 1
    else:
        print(f"  No change: {pyfile}")

print("=" * 60)
print(f"\nUpdated {updated_count} files")
print("All .txt file paths now point to txt/ directory")
