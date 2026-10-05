# split a python file into chunks of functions and return their names

import ast
from pathlib import Path


def extract_functions(file_path):
    source = Path(file_path).read_text(encoding="utf-8")
    # parse the source code into string and then into an AST (Abstract Syntax Tree)
    tree = ast.parse(source)

    chunks = []
    for node in ast.walk(tree): # walk through all nodes in the AST
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            chunks.append({
                "name": node.name,
                "file": str(file_path),
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "code": ast.get_source_segment(source, node),
            })
    return chunks


if __name__ == "__main__":
    repo = Path("../tractian_dashboard")
    for py_file in repo.rglob("*.py"):
        for c in extract_functions(py_file):
            print(f"{c['name']:<16} {c['file']}:{c['start_line']}-{c['end_line']}")