from .defs import Orientation
from .permutation import Permutation


class PgonEdge:
    def __init__(self) -> None:
        self._perm = Permutation()
        self._orientation = 0
        self._adjEdgeId = 0

    def setNumColors(self, numColors: int):
        self._perm.setSize(numColors)

    def setOrientation(self, o: Orientation):
        self._orientation = o

    def setAdjEdgeId(self, edge):
        self._adjEdgeId = edge

    def colorPerm(self) -> Permutation:
        return self._perm
