from PyQt6.QtWidgets import QGraphicsView

from .diagram_view import DiagramView


# class PoincareView(Q3CanvasView,DiagramView):
# Need to find a replacement for Q3CanvasView
# https://doc.qt.io/archives/qt-4.8/graphicsview-porting.html
# QGraphicsView class provides a widget for displaying the contents of a QGraphicsScene.
class PoincareView(QGraphicsView, DiagramView):
    def __init__(self, parent, name) -> None:
        super().__init__()
        self.parent = parent
        self.name = name
        pass
