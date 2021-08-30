from pathlib import Path
from typing import Optional

import libcst as cst
import libcst.matchers as m
from libcst import (
    Param,
    Annotation,
    Subscript,
    Name,
)


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
        with open(file_path, "r") as file:
            old = file.read()
            new = convert_file(old)

        with open(file_path, "w") as file:
            file.write(new)
            if old != new:
                changed_files += 1

    return changed_files


def convert_file(py_source: str) -> str:
    source_tree = cst.parse_module(py_source)
    transformer = ConvertTransformer()
    modified_tree = source_tree.visit(transformer)
    return modified_tree.code


class ConvertTransformer(cst.CSTTransformer):
    def __init__(self) -> None:
        super().__init__()
        self.optional_import_name = None

    def visit_ImportFrom_names(self, node: cst.ImportFrom) -> None:
        if (
                node.module.value == 'typing'
        ):
            for import_alias in node.names:
                if import_alias.name.value == "Optional":
                    self.optional_import_name = (
                        import_alias.asname.name
                        if import_alias.asname
                        else import_alias.name
                    )

    def visit_Import_names(self, node: cst.Import) -> None:
        for import_alias in node.names:
            if import_alias.name.value == "typing":
                typing_name = (
                    import_alias.asname.name
                    if import_alias.asname
                    else import_alias.name
                )
                # todo convert to structur to write

    def leave_Param(
            self, original_node: Param, updated_node: Param
    ) -> Param:
        annotation = updated_node.annotation.annotation
        if m.matches(updated_node.default, m.Name("None")) and not (
                isinstance(annotation, Subscript)
                and cst.ensure_type(annotation.value, Name).value == "Optional"
        ):
            return updated_node.with_changes(
                annotation=Annotation(
                    Subscript(
                        value=self.optional_import_name,
                        slice=[cst.SubscriptElement(cst.Index(annotation))],
                    )
                )
            )
        return updated_node
