from .diagram import Diagram


class RegularPgon(Diagram):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Regular Polygon"
        
    def setNumLayers(self, numLayers: int) -> None:
        self.numLayers = numLayers
