from enum import Enum


class ReflSymType(Enum):
    REFL_NONE = 0
    REFL_EDGE_BISECTOR = 1
    REFL_PGON_RADIUS = 2


# enum ReflSymType
# {
REFL_NONE = 0
REFL_EDGE_BISECTOR = 1
REFL_PGON_RADIUS = 2
# };


class Orientation(Enum):
    """
    in the old code -ve values meant reflection and +ve meant rotation

    Args:
        Enum (_type_): _description_
    """

    REFLECTION = -1
    ROTATION = 1


# # enum Orientation
# {
REFLECTION = -1
ROTATION = 1
# };


class Exposure(Enum):
    MINEXPOSURE = 0
    MAXEXPOSURE = 1


# enum Exposure
# {
MINEXPOSURE = 0
MAXEXPOSURE = 1
# };

# // used for runtime type identification


class ElemType(Enum):
    ELEMENT = 0
    EUCLID_POLYLINE = 1
    EUCLID_POLY = 2
    CIRCLE = 3
    HYPER_POLYLINE = 4
    HYPER_POLY = 5


# enum ElemType
# {
ELEMENT = 0
EUCLID_POLYLINE = 1
EUCLID_POLY = 2
CIRCLE = 3
HYPER_POLYLINE = 4
HYPER_POLY = 5
# # };


class ZoomType(Enum):
    IN = -1
    OUT = 1
    DEFAULT = 2


# enum ZoomType
# {
IN = -1
OUT = 1
DEFAULT = 2
# };


class PanType(Enum):
    PAN_LEFT = 0
    PAN_RIGHT = 1
    PAN_UP = 2
    PAN_DOWN = 3


# enum PanType
# {
PAN_LEFT = 0
PAN_RIGHT = 1
PAN_UP = 2
PAN_DOWN = 3
# };


class ViewMode(Enum):
    """
    Args:
        Enum (_type_): _description_
    """

    NORMAL = 0  # no animation, no editing
    ANIMATE = (1,)
    EDIT = 2


# enum ViewMode
# {
NORMAL = 0  # no animation, no editing
ANIMATE = (1,)
EDIT = 2
# };


class DiagramType(Enum):
    """
    Args:
        Enum (_type_): _description_
    """

    DIAGRAM = 0  # abstract diagram
    REGULAR_PGON = 1
    IRREGULAR_PGON = 2


#     // etc
# enum DiagramType
# {
DIAGRAM = 0  # abstract diagram
REGULAR_PGON = 1
IRREGULAR_PGON = 2
#     // etc
# };


class LineStyle(Enum):
    SOLID = 0
    DOTS = 1


# enum LineStyle
# {
SOLID = 0
DOTS = 1
# };
