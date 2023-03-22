import ast
import os


def get_functions(file_path):
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append((node.name, node, node.end_lineno-node.lineno))

    return functions


def go_over_directory(directory_path):
    with os.scandir(directory_path) as itr:
        for entry in itr:
            if entry.name.endswith(".py"):
                try:
                    functions = get_functions(os.path.join(entry.path))
                except:
                    # I got errors on py files in dependency folders
                    continue

                for name, node, length in functions:
                    # TODO move to _filter function
                    if 'test' in name or 'test' in entry.path\
                            or '__' in name or '__' in entry.path:
                        continue
                    if length >= 200:
                        print(f'{entry.name}|{name}: {length}')
            else:
                if entry.is_dir():
                    go_over_directory(entry.path)


if __name__ == '__main__':
    go_over_directory("folder/path")

