import os

def generate_project_structure(root_path, output_file, indent="│   ", branch="├── ", last_branch="└── "):
    ignore_folders = {'env'}  # Add more if needed

    def walk(dir_path, prefix=""):
        entries = os.listdir(dir_path)
        entries = [e for e in entries if e not in ignore_folders]
        entries.sort()
        for index, entry in enumerate(entries):
            path = os.path.join(dir_path, entry)
            is_last = index == len(entries) - 1
            connector = last_branch if is_last else branch
            line = f"{prefix}{connector}{entry}\n"
            lines.append(line)
            if os.path.isdir(path):
                extension = "    " if is_last else indent
                walk(path, prefix + extension)

    lines = [f"{os.path.basename(root_path)}/\n"]
    walk(root_path)
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

# USAGE EXAMPLE
root_folder = r"D:\Python Practice\IndexIQ"  # Update to your project root
output_txt = "project_structure.txt"

generate_project_structure(root_folder, output_txt)
print(f"Structure written to {output_txt}")
