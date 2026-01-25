import os
import argparse

def print_tree(root, prefix="", depth=0, max_depth=3):
    if depth > max_depth:
        return

    entries = sorted(os.listdir(root))
    entries = [e for e in entries if not e.startswith('.')]  # Skip hidden files

    for index, entry in enumerate(entries):
        path = os.path.join(root, entry)
        connector = "└── " if index == len(entries) - 1 else "├── "
        print(prefix + connector + entry)

        if os.path.isdir(path):
            extension = "    " if index == len(entries) - 1 else "│   "
            print_tree(path, prefix + extension, depth + 1, max_depth)

def main():
    parser = argparse.ArgumentParser(description="Print the directory structure of a folder.")
    parser.add_argument("folder", type=str, help="Path to the folder")
    parser.add_argument("--max-depth", type=int, default=3, help="Maximum depth to display (default: 3)")

    args = parser.parse_args()
    root_path = args.folder

    if not os.path.isdir(root_path):
        print(f"Error: '{root_path}' is not a valid directory.")
        return

    print(os.path.basename(os.path.abspath(root_path)) + "/")
    print_tree(root_path, depth=1, max_depth=args.max_depth)

if __name__ == "__main__":
    main()
