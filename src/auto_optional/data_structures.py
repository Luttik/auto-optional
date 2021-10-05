from typing import List, Union

import libcst as cst


class BestImportStatementFirstList(List[Union[cst.Name, cst.Attribute]]):
    def append(self, x: Union[cst.Name, cst.Attribute]) -> None:
        if self and isinstance(x, cst.Name) and isinstance(self[0], cst.Attribute):
            super().insert(0, x)

        return super().append(x)
