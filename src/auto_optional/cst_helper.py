from typing import List, Optional, Sequence, Type

import libcst as cst


def unwrap_commutative_binary_operator(
    operation_node: cst.BinaryOperation,
    operator: Optional[Type[cst.BaseBinaryOp]] = None,
) -> List[cst.BaseExpression]:
    def unwrap_or_return(node: cst.BaseExpression) -> List[cst.BaseExpression]:
        if isinstance(node, cst.BinaryOperation) and isinstance(
            node.operator, operator
        ):
            return unwrap_commutative_binary_operator(node, operator)
        return [node]

    if operator is None:
        operator = type(operation_node.operator)

    return [
        *unwrap_or_return(operation_node.left),
        *unwrap_or_return(operation_node.right),
    ]
