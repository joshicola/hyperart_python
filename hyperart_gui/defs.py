"""Definitions for the GUI."""
from enum import Enum


class ReflSymType(Enum):
    """Reflection Symmetry Types"""

    REFL_NONE = 0
    REFL_EDGE_BISECTOR = 1
    REFL_PGON_RADIUS = 2


class Orientation(Enum):
    """
    Orientation of the reflection.
    in the old code -ve values meant reflection and +ve meant rotation

    Args:
        Enum (_type_): _description_
    """

    REFLECTION = -1
    ROTATION = 1


class Exposure(Enum):
    """TODO: Expose or hide the element"""

    MINEXPOSURE = 0
    MAXEXPOSURE = 1


class ElemType(Enum):
    """Element Types
    Used for runtime type identification
    """

    ELEMENT = 0
    EUCLID_POLYLINE = 1
    EUCLID_POLY = 2
    CIRCLE = 3
    HYPER_POLYLINE = 4
    HYPER_POLY = 5


class ZoomType(Enum):
    """Zoom Types"""

    IN = -1
    OUT = 1
    DEFAULT = 2


class PanType(Enum):
    """Pan Types"""

    PAN_LEFT = 0
    PAN_RIGHT = 1
    PAN_UP = 2
    PAN_DOWN = 3


class ViewMode(Enum):
    """
    Viewing Modes
    """

    NORMAL = 0  # no animation, no editing
    ANIMATE = (1,)
    EDIT = 2


class DiagramType(Enum):
    """Diagram Types"""

    DIAGRAM = 0  # abstract diagram
    REGULAR_PGON = 1
    IRREGULAR_PGON = 2


class LineStyle(Enum):
    """Line Styles"""

    SOLID = 0
    DOTS = 1
