#!/usr/bin/env python3
"""
Script to copy all files from a folder and its subfolders into a single flat folder.
"""

import os
import shutil
import sys
from pathlib import Path


def flatten_folder(source_path, target_folder_name="flattened_files"):
    """
    Copy all files from source_path and its subfolders into a single flat folder.
    
    Args:
        source_path: Path to the source folder
        target_folder_name: Name of the target folder (default: "flattened_files")
    """
    source = Path(source_path).resolve()
    
    if not source.exists():
        print(f"Error: Source path '{source}' does not exist!")
        return False
    
    if not source.is_dir():
        print(f"Error: Source path '{source}' is not a directory!")
        return False
    
    # Create target folder in the same parent directory as source
    target = source.parent / target_folder_name
    
    # Create target directory if it doesn't exist
    target.mkdir(exist_ok=True)
    print(f"Target folder: {target}")
    
    copied_count = 0
    skipped_count = 0
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(source):
        for filename in files:
            source_file = Path(root) / filename
            target_file = target / filename
            
            # Handle duplicate filenames by adding a number
            if target_file.exists():
                base_name = target_file.stem
                extension = target_file.suffix
                counter = 1
                
                while target_file.exists():
                    new_name = f"{base_name}_{counter}{extension}"
                    target_file = target / new_name
                    counter += 1
                
                print(f"Renamed: {filename} -> {target_file.name}")
            
            try:
                shutil.copy2(source_file, target_file)
                copied_count += 1
                print(f"Copied: {source_file.relative_to(source)} -> {target_file.name}")
            except Exception as e:
                print(f"Error copying {source_file}: {e}")
                skipped_count += 1
    
    print(f"\nDone! Copied {copied_count} files to '{target}'")
    if skipped_count > 0:
        print(f"Skipped {skipped_count} files due to errors")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python flatten_files.py <source_folder> [target_folder_name]")
        print("\nExample:")
        print("  python flatten_files.py /path/to/folder")
        print("  python flatten_files.py /path/to/folder my_flat_folder")
        sys.exit(1)
    
    source_path = sys.argv[1]
    target_folder_name = sys.argv[2] if len(sys.argv) > 2 else "flattened_files"
    
    flatten_folder(source_path, target_folder_name)


if __name__ == "__main__":
    main()
