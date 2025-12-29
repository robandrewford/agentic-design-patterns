import os
import re
import glob

NOTEBOOKS_DIR = "notebooks"

def clean_filename(filename):
    # Get the basename without extension
    base = os.path.basename(filename)
    name_no_ext = os.path.splitext(base)[0]
    
    match = re.match(r"^(\d+)", name_no_ext)
    if not match:
        # Fallback: try to find "Chapter X"
        match_chapter = re.search(r"Chapter\s*(\d+)", name_no_ext, re.IGNORECASE)
        if match_chapter:
             num = match_chapter.group(1)
        else:
             print(f"Skipping {filename}: No leading number found")
             return None, None
    else:
        num = match.group(1)
    
    # Pad number to at least 2 digits
    padded_num = num.zfill(2)
    
    # Rest of the string after the number
    rest = name_no_ext[len(num):]
    
    # Remove "Chapter", "chapter", "Code Example", "CodeExample" variants
    # Also remove "Prompt" if it appears redundantly like "1_Prompt_Chapter 1..."
    # We want to be a bit aggressive in cleaning noise
    rest = re.sub(r'[_\-\s]Chapter[_\-\s]\d*', '_', rest, flags=re.IGNORECASE)
    rest = re.sub(r'[_\-\s]Code[_\-\s]?Example', '_', rest, flags=re.IGNORECASE)
    
    # Replace non-alphanumeric (except underscores) with underscores
    # Logic: spaces, hyphens, parentheses -> underscore
    rest = re.sub(r"[^a-zA-Z0-9]", "_", rest)
    
    # Convert to lowercase
    rest_clean = rest.lower()
    
    # Remove multiple underscores
    rest_clean = re.sub(r"_+", "_", rest_clean)
    
    # Strip leading/trailing underscores
    rest_clean = rest_clean.strip("_")
    
    new_name = f"{padded_num}_{rest_clean}.py"
    return filename, os.path.join(os.path.dirname(filename), new_name)

def main():
    print("Starting cleanup...")
    
    # 1. Remove .ipynb files
    ipynb_files = glob.glob(os.path.join(NOTEBOOKS_DIR, "*.ipynb"))
    for f in ipynb_files:
        print(f"Removing {f}")
        try:
            os.remove(f)
        except OSError as e:
            print(f"Error removing {f}: {e}")

    # 2. Rename .py files
    py_files = glob.glob(os.path.join(NOTEBOOKS_DIR, "*.py"))
    
    for f in py_files:
        old_path, new_path = clean_filename(f)
        
        if not new_path:
            continue
            
        if old_path == new_path:
            continue
            
        # Prevent overwriting if target exists (append suffix if needed, though unlikely here)
    # Handle case-insensitive file systems (like macOS) by checking if it's the same file
        # Handle case-insensitive file systems (like macOS) by checking if it's the same file
        if os.path.exists(new_path) and old_path != new_path:
            # Check if they are the same file (case-insensitive match)
            if os.path.normcase(os.path.abspath(old_path)) == os.path.normcase(os.path.abspath(new_path)):
                 # Rename to temp then to target
                 temp_path = new_path + ".tmp"
                 print(f"Renaming (case fix): {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
                 os.rename(old_path, temp_path)
                 os.rename(temp_path, new_path)
                 continue
            else:
                 print(f"WARNING: Target {new_path} exists and is different. Skipping {old_path}")
                 continue

        print(f"Renaming: {os.path.basename(old_path)} -> {os.path.basename(new_path)}")
        try:
            os.rename(old_path, new_path)
        except OSError as e:
            print(f"Error renaming {old_path}: {e}")
            
    print("Cleanup complete.")

if __name__ == "__main__":
    main()
