import os

def print_directory_structure(root):
    for root, dirs, files in os.walk(root):
        level = root.replace(root, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

dataset_path = "./dataset"
print_directory_structure(dataset_path)
