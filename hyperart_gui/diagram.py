from PyQt6.QtGui import QTextDocument

from .pattern import Pattern
from .pgonedge import PgonEdge


class Diagram(QTextDocument):
    """_summary_"""

    def __init__(self) -> None:
        """_summary_"""
        super().__init__()
        self.name = "Diagram"
        self._p = 0
        self.edges = []
        self._fileName = ""
        self._numColors = 0
        self._fundPat_ = Pattern()  # fundametal pattern

        # setNumColors has to be called to initialize these
        self._colorMap = {}

        # /**
        # Number of Layers to generate
        # */
        self._numLayers = 0
        # /**
        # diag_ is collection of all the patterns.
        # */
        self._diag = {}
        self._layers = []

    def p(self) -> int:
        return self._p

    def setP(self, v: int):
        self._p = v

        for _ in range(self._p):
            e = PgonEdge()
            e.setNumColors(self._numColors)
            self.edges.append(e)

    def numColors(self) -> int:
        return self._numColors

    def fundPat(self) -> Pattern:
        return self._fundPat_

    def setColorMapValue(self, cid, c):
        self._colorMap[cid] = c
