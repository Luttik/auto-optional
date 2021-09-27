from pathlib import Path

import libcst as cst

from auto_optional.code_processing import AutoOptionalTransformer


def convert_path(path: Path) -> int:
    """
    Converts all files in the Path.

    :return: The amount of changed files.
    """
    changed_files = 0

    files = []

    if path.is_file():
        files.append(path)
    else:
        files.extend(path.glob("**/*.py"))

    for file_path in files:
        print(f"Reading file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as file:
            old = file.read()
            new = convert_file(old)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new)
            if old != new:
                changed_files += 1

    return changed_files


def convert_file(py_source: str) -> str:
    source_tree = cst.metadata.MetadataWrapper(cst.parse_module(py_source))
    modified_tree = source_tree.visit(AutoOptionalTransformer())
    return modified_tree.code
