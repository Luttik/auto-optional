from typing import Union

import libcst as cst
import libcst.matchers as m

from auto_optional.cst_helper import unwrap_commutative_binary_operator
from auto_optional.data_structures import BestImportStatementFirstList


class ImportStatementChecker:
    import_names: BestImportStatementFirstList
    imported_module: str
    imported_value: str

    def __init__(self, imported_module: str, imported_object: str) -> None:
        super().__init__()
        # Will be a list of all existing import statements
        # that references the desired type
        self.import_names = BestImportStatementFirstList()
        self.imported_module = imported_module
        self.imported_value = imported_object

    def get_import_name(self) -> Union[cst.Name, cst.Attribute]:
        return self.import_names[0]

    def check_import_from(self, node: cst.ImportFrom) -> None:
        assert node.module
        if node.module.value == self.imported_module:
            if isinstance(node.names, cst.ImportStar):
                # When ``from module import *`` is found the
                self.import_names.append(cst.Name(self.imported_value))
            else:
                for import_alias in node.names:
                    if import_alias.name.value == self.imported_value:
                        self.import_names.append(
                            cst.ensure_type(import_alias.asname.name, cst.Name)
                            if import_alias.asname
                            else import_alias.name
                        )

    def check_import(self, node: cst.Import) -> None:
        for import_alias in node.names:
            if import_alias.name.value == self.imported_module:
                typing_name = (
                    cst.ensure_type(import_alias.asname.name, cst.Name)
                    if import_alias.asname
                    # ensure_type to satisfy mypy
                    # it is a Name since its value equals the module (see if statement)
                    else cst.ensure_type(import_alias.name, cst.Name)
                )

                self.import_names.append(
                    cst.Attribute(
                        value=cst.Name(typing_name.value),
                        attr=cst.Name(self.imported_value),
                    )
                )


class AutoOptionalTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (cst.metadata.QualifiedNameProvider,)

    def __init__(self) -> None:
        super().__init__()
        self.optional_import_checker = ImportStatementChecker("typing", "Optional")
        self.union_import_checker = ImportStatementChecker("typing", "Union")

        # Will be set to true if there if we find an non-optional param with None
        # as default i.e. ``def foo(bar: str = None)``.
        self.optional_import_needed = False

    def visit_ImportFrom_names(self, node: cst.ImportFrom) -> None:
        """Searches for imports of ``typing.Optional`` and stores for later use"""
        self.optional_import_checker.check_import_from(node)
        self.union_import_checker.check_import_from(node)

    def visit_Import_names(self, node: cst.Import) -> None:
        """Searches for imports of ``typing`` and stores for later use"""
        self.optional_import_checker.check_import(node)
        self.union_import_checker.check_import(node)

    def visit_Param(self, node: cst.Param) -> None:
        """
        Used to detect if there are any statements that need to be changed to Optional
        """
        if (
            node.default
            and m.matches(node.default, m.Name("None"))
            and not self.optional_import_checker.import_names
        ):
            # TODO add check for the ``Optional[None]`` alternative
            self.optional_import_needed = True

    def leave_Module(
        self, original_node: cst.Module, updated_node: cst.Module
    ) -> cst.Module:
        """
        The last call that is handled in the process of parsing and converting the code.

        Is only used to add the ``typing.Optional`` import statement when missing.
        """
        if (
            not self.optional_import_checker.import_names
            or not self.optional_import_needed
        ):
            return updated_node

        import_statement = self.__build_import_statement()
        import_statement_location = self.__find_line_for_optional_import_insertion(
            updated_node
        )
        return updated_node.with_changes(
            body=[
                *updated_node.body[:import_statement_location],
                import_statement,
                *updated_node.body[import_statement_location:],
            ]
        )

    def __build_import_statement(self) -> cst.SimpleStatementLine:
        return cst.SimpleStatementLine(
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

    def __find_line_for_optional_import_insertion(
        self, updated_node: cst.Module
    ) -> int:
        insert_at = 0
        for index, body_part in enumerate(updated_node.body):
            if (
                isinstance(body_part, cst.SimpleStatementLine)
                and len(body_part.children) > 0
                and (
                    (  # module level docstring
                        index == 0
                        and m.matches(body_part.children[0], m.Expr(m.SimpleString()))
                    )
                    or m.matches(  # future import
                        body_part.children[0],
                        m.ImportFrom(module=m.Name("__future__")),
                    )
                )
            ):
                # module docstring
                insert_at += 1
            elif index > 1:
                break
        return insert_at

    def __check_if__union_none(self, annotation: cst.BaseExpression) -> bool:
        #  Return if it is a Union[..., None, ...] statement
        return bool(
            # Check if Union can even be imported
            self.union_import_checker.import_names
            # Check if it is a Union statement at all
            and (
                isinstance(annotation, cst.Subscript)
                and m.matches(
                    annotation.value,
                    self.union_import_checker.get_import_name(),  # type: ignore
                )
            )
            # Check if any of the slice items is None
            and any(
                (
                    isinstance(item.slice, cst.Index)
                    and isinstance(item.slice.value, cst.Name)
                    and item.slice.value.value == "None"
                )
                for item in annotation.slice
            )
        )

    def __check_if__or_none(self, annotation: cst.BaseExpression) -> bool:
        return (
            isinstance(annotation, cst.BinaryOperation)
            and isinstance(annotation.operator, cst.BitOr)
            and any(
                m.matches(option, m.Name(value="None"))
                for option in unwrap_commutative_binary_operator(annotation)
            )
        )

    def leave_Param(
        self, original_node: cst.Param, updated_node: cst.Param
    ) -> cst.Param:
        """
        Changes Parameters of type ``x`` to ``Optional[x]`` if their default is None.
        """
        if (  # Check if optional is required
            updated_node.annotation
            and updated_node.default
            and m.matches(updated_node.default, m.Name("None"))
        ):
            annotation = updated_node.annotation.annotation

            # TODO if ``Union[None]`` return None

            # Also allow Union
            if self.__check_if__union_none(annotation) or self.__check_if__or_none(
                annotation
            ):
                return updated_node

            if not self.optional_import_checker.import_names:
                self.optional_import_checker.import_names.append(cst.Name("Optional"))

            if not (
                isinstance(annotation, cst.Subscript)
                and any(
                    m.matches(annotation.value, optional_import)  # type: ignore
                    for optional_import in self.optional_import_checker.import_names
                )
            ):
                return updated_node.with_changes(
                    annotation=cst.Annotation(
                        cst.Subscript(
                            value=(self.optional_import_checker.get_import_name()),
                            slice=[cst.SubscriptElement(cst.Index(annotation))],
                        )
                    )
                )
        return updated_node
