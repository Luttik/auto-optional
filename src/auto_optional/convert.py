from pathlib import Path

import libcst as cst
import libcst.matchers as m


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
    source_tree = cst.parse_module(py_source)
    modified_tree = source_tree.visit(AutoOptionalTransformer())
    return modified_tree.code


class BestFirstList(list):
    def append(self, x: cst.CSTNode) -> None:
        if self and isinstance(x, cst.Name) and isinstance(self[0], cst.Attribute):
            super().insert(0, x)

        return super().append(x)


class AutoOptionalTransformer(cst.CSTTransformer):
    def __init__(self) -> None:
        super().__init__()
        # Will be a list of all existing import statements that references
        # ``typing.Optional`` or, if not available, just``typing``.
        self.optional_import_names = BestFirstList()

        # Will be set to true if there if we find an non-optional param with None
        # as default i.e. ``def foo(bar: str = None)``.
        self.optional_import_needed = False

    def visit_ImportFrom_names(self, node: cst.ImportFrom) -> None:
        """Searches for imports of ``typing.Optional`` and stores for later use"""
        assert node.module
        if node.module.value == "typing":
            if isinstance(node.names, cst.ImportStar):
                # When ``from typing import *`` is found
                self.optional_import_names.append(cst.Name("Optional"))
            else:
                for import_alias in node.names:
                    if import_alias.name.value == "Optional":
                        self.optional_import_names.append(
                            import_alias.asname.name
                            if import_alias.asname
                            else import_alias.name
                        )

    def visit_Import_names(self, node: cst.Import) -> None:
        """Searches for imports of ``typing`` and stores for later use"""
        for import_alias in node.names:
            if import_alias.name.value == "typing":
                typing_name = (
                    cst.ensure_type(import_alias.asname.name, cst.Name)
                    if import_alias.asname
                    # ensure_type to satisfy mypy
                    # it is a Name since its value equals "typing" (see if statement)
                    else cst.ensure_type(import_alias.name, cst.Name)
                )

                self.optional_import_names.append(
                    cst.Attribute(
                        value=cst.Name(typing_name.value), attr=cst.Name("Optional")
                    )
                )

    def visit_Param(self, node: cst.Param) -> None:
        """
        Used to detect if there are any statements that need to be changed to Optional
        """
        if (
            node.default
            and m.matches(node.default, m.Name("None"))
            and not self.optional_import_names
        ):
            self.optional_import_needed = True

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        """
        The last call that is handled in the process of parsing and converting the code.

        Is only used to add the ``typing.Optional`` import statement when missing.
        """
        if self.optional_import_names and self.optional_import_needed:
            import_statement = cst.SimpleStatementLine(
                body=[
                    cst.ImportFrom(
                        module=cst.Name(
                            value="typing",
                        ),
                        names=[
                            cst.ImportAlias(
                                name=cst.Name(
                                    value="Optional",
                                ),
                            ),
                        ],
                    )
                ]
            )
            return updated_node.with_changes(
                body=[import_statement, *updated_node.body]
            )
        return updated_node

    def leave_Param(
        self, original_node: cst.Param, updated_node: cst.Param
    ) -> cst.Param:
        """
        Changes Parameters of type ``x`` to ``Optional[x]`` if their default is None.
        """
        if updated_node.annotation:
            if len(self.optional_import_names) > 1:
                print("x")
            annotation = updated_node.annotation.annotation
            if updated_node.default and m.matches(updated_node.default, m.Name("None")):
                if not self.optional_import_names:
                    self.optional_import_names.append(cst.Name("Optional"))

                if not (
                    isinstance(annotation, cst.Subscript)
                    and any(
                        m.matches(annotation.value, optional_import)
                        for optional_import in self.optional_import_names
                    )
                ):
                    return updated_node.with_changes(
                        annotation=cst.Annotation(
                            cst.Subscript(
                                value=self.optional_import_names[0],
                                slice=[cst.SubscriptElement(cst.Index(annotation))],
                            )
                        )
                    )
        return updated_node
