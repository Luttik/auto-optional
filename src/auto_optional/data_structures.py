import libcst as cst


class BestFirstList(list):
    def append(self, x: cst.CSTNode) -> None:
        if self and isinstance(x, cst.Name) and isinstance(self[0], cst.Attribute):
            super().insert(0, x)

        return super().append(x)
