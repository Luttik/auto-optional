from typing import List, Optional, Type

import libcst as cst


def unwrap_commutative_binary_operator(
    operation_node: cst.BinaryOperation,
    operator: Optional[Type[cst.BaseBinaryOp]] = None,
) -> List[cst.BaseExpression]:
    # Created a new variable to satisfy mypy
    operator_not_null = operator or type(operation_node.operator)

    def unwrap_or_return(node: cst.BaseExpression) -> List[cst.BaseExpression]:
        if isinstance(node, cst.BinaryOperation) and isinstance(
            node.operator, operator_not_null
        ):
            return unwrap_commutative_binary_operator(node, operator_not_null)
        return [node]

    return [
        *unwrap_or_return(operation_node.left),
        *unwrap_or_return(operation_node.right),
    ]
