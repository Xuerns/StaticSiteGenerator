import sys
import os
import shutil

try:
    from copystatic import copy_files_recursive
except ImportError:
    from src.copystatic import copy_files_recursive

try:
    from generate_page import generate_pages_recursive
except ImportError:
    from src.generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    print(f"Generating pages with basepath '{basepath}'...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, basepath)


if __name__ == "__main__":
    main()
