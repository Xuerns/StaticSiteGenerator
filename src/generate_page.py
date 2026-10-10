import os

try:
    from markdown_blocks import markdown_to_html_node
except ImportError:
    from src.markdown_blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found")


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    node = markdown_to_html_node(markdown_content)
    html_content = node.to_html()

    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_content
    )
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str = "/"
):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                dest_html_path = dest_path[:-3] + ".html"
                generate_page(from_path, template_path, dest_html_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
