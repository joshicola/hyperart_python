from PyQt6.QtGui import QPainter, QTextDocument


class DiagramView:
    def __init__(self) -> None:
        self.docViewer = None
        self.dgram = None
        pass

    def setDocument(self, doc: QTextDocument) -> None:
        pass

    def print(self, p: QPainter) -> None:
        pass

    def saveAs(self, fileName: str) -> None:
        pass
