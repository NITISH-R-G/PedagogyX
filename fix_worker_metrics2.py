import glob

def add_type_ignore(filepath, search_str):
    with open(filepath, 'r') as f:
        content = f.read()

    if search_str in content and search_str + '  # type: ignore' not in content:
        content = content.replace(search_str, search_str + '  # type: ignore')

    with open(filepath, 'w') as f:
        f.write(content)

add_type_ignore('packages/capture-core/py/pedagogyx_core/models.py', 'from pydantic')
