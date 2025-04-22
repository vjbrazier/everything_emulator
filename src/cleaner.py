import os, re, shutil

def remove_name_filler(name):
    # List of unwanted region/language tags
    filler_data = [
        'En', 'Fr', 'Es', 'It', 'Js', 'De',
        'Europe', 'Japan', '(World)', 'Asia', 'Australia', 'USA'
    ]

    # Step 1: Remove filler items from grouped language/region lists like (En,Fr,De)
    def clean_lang_group(match):
        items = [i.strip() for i in match.group(1).split(',')]
        kept = [i for i in items if i not in filler_data]
        return f"({', '.join(kept)})" if kept else ''

    name = re.sub(r'\(([^)]+)\)', clean_lang_group, name)

    # Step 2: Remove any remaining standalone filler tokens with common separators
    pattern = r'(\s*[\(\[\-_]?\b(?:' + '|'.join(re.escape(item) for item in filler_data if item != 'USA') + r')\b[\)\]_]*\s*)'
    name = re.sub(pattern, ' ', name, flags=re.IGNORECASE)

    # Step 3: Remove empty parentheses, brackets, dashes, or stray commas
    name = re.sub(r'[\(\[\{][\s,]*[\)\]\}]', '', name)      # Empty ()
    name = re.sub(r'\s{2,}', ' ', name)                     # Extra spaces
    name = re.sub(r'[\s,\-]+$', '', name)                   # Trailing commas/dashes
    name = name.strip()

    return name.replace('(World)', '').strip()


folder_path = 'temp'
trash_folder = os.path.join(folder_path, 'Trash')

# Create Trash folder if it doesn't exist
os.makedirs(trash_folder, exist_ok=True)

# Collect and group files by their cleaned names
file_groups = {}

for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    if os.path.isfile(filepath) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        name_part, ext = os.path.splitext(filename)
        cleaned_name = remove_name_filler(name_part)
        key = cleaned_name.lower()
        file_groups.setdefault(key, []).append((filename, name_part, ext))

# Process each group
for group, files in file_groups.items():
    if len(files) == 1:
        filename, name_part, ext = files[0]
        new_name = remove_name_filler(name_part) + ext
        if new_name != filename:
            os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
            print(f"Renamed: {filename} → {new_name}")
    else:
        # Prefer USA version
        usa_file = None
        for f in files:
            if 'USA' in f[1]:
                usa_file = f
                break

        if usa_file:
            filename, name_part, ext = usa_file
            new_name = remove_name_filler(name_part) + ext
            if new_name != filename:
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
                print(f"Renamed (USA): {filename} → {new_name}")
            # Move the rest to Trash
            for f in files:
                if f != usa_file:
                    shutil.move(os.path.join(folder_path, f[0]), os.path.join(trash_folder, f[0]))
                    print(f"Moved to Trash: {f[0]}")
        else:
            # No USA version found, keep the first, move others to Trash
            keep = files[0]
            filename, name_part, ext = keep
            new_name = remove_name_filler(name_part) + ext
            if new_name != filename:
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))
                print(f"Renamed (fallback): {filename} → {new_name}")
            for f in files[1:]:
                shutil.move(os.path.join(folder_path, f[0]), os.path.join(trash_folder, f[0]))
                print(f"Moved to Trash (fallback): {f[0]}")