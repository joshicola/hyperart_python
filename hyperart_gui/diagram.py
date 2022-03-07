from PyQt6.QtGui import QTextDocument


class Diagram(QTextDocument):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Diagram"
