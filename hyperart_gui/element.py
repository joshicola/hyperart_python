"""
/***************************************************************************
 *   Copyright (C) 2005 by Dr. Douglas Dunham, Ajit Datar                  *
 *   ddunham@d.umn.edu , data0003@d.umn.edu                                *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  *
 *                                                                         *
 ***************************************************************************/
"""
import copy
import logging
from decimal import DivisionByZero

import numpy as np
from idna import InvalidCodepoint

from .defs import ElemType, LineStyle
from .transformation import Transformation

log = logging.getLogger(__name__)


class Point:
    """
    Point can be used either as a poincaré point (x,y)
    or as a weierstrass point (x,y,w), or anything other.
    """

    def __init__(self, x=None, y=None):
        self._x = x if x is not None else 0
        self._y = y if y is not None else 0
        self._w = 0
        self._type = 0

    def x(self) -> float:
        """Return the x coordinate of the point.

        Returns:
            float: x coordinate of the point.
        """
        return self._x

    def y(self) -> float:
        """Return the y coordinate of the point.

        Returns:
            float: y coordinate of the point.
        """
        return self._y

    def w(self) -> float:
        """Return the weierstrass parameter.

        Returns:
            float: Weierstrass parameter.
        """
        return self._w

    def type(self) -> str:
        """
        type can be used as an identifier of
        what this point is being used as.
        eg poincare/weierstrass or any other use

        Returns:
            str: The type of point poincare/weierstrass
        """
        return self._type

    def setX(self, x: float):
        """Set the x coordinate of the point.

        Args:
            x (float): x coordinate of the point.
        """
        self._x = x

    def setY(self, y: float):
        """Set the y coordinate of the point.

        Args:
            y (float): y coordinate of the point.
        """
        self._y = y

    def setW(self, w: float):
        """
        Set the weierstrass parameter.

        Args:
            w (float): Weierstrass parameter.
        """
        self._w = w

    def setType(self, t: str):
        """Set the type of the point.

        Args:
            t (str): The type of the point, poincare/weierstrass.
        """
        self._type = t

    def poincareToWeierstrass(self):
        """
        Convert a poincaré point to a weierstrass point.
        """
        if "weierstrass" == self._type:
            return

        elif "poincare" != self._type:
            log.warning(
                "Point::poincareToWeierstrass() : point is not in poincare mode"
            )
            return

        s = self._x * self._x + self._y * self._y
        if 1.0 == s:
            raise DivisionByZero(
                "Point::poincareToWeierstrass() " ": possible divide by zero error"
            )

        self._x = 2.0 * self._x / (1.0 - s)
        self._y = 2.0 * self._y / (1.0 - s)
        self._w = (1.0 + s) / (1.0 - s)
        self._type = "weierstrass"

    def weierstrassToPoincare(self):
        """
        Convert a weierstrass point to a poincaré point.
        """
        denom = 1.0 + self._w
        self._x = self._x / denom
        self._y = self._y / denom
        self._w = 0.0
        self._type = "poincare"

    def transform(self, t: Transformation):
        """
        Apply a transformation to a point.

        Args:
            t (Transformation): Transformation to apply.
        """
        self._x = t.transformX(self._x, self._y)
        self._y = t.transformY(self._x, self._y)
        self._w = t.transformW(self._x, self._y, self._w)
        self._type = t.transformType(self._type)


def weierstrassCrossProduct(p1: Point, p2: Point) -> Point:
    """
    Returns a dot product in weierstrass space.
    If both p1 and p2 aren't in weierstrass, then a point (0,0,0) is returned.
    """
    r = Point()

    if "weierstrass" != p1.type() | "weierstrass" != p2.type():
        log.warning("weierstrassDotProduct : both points should be weierstrass points")
        return r
    r.setX(p1.y() * p2.w() - p1.w() * p2.y())
    r.setY(p1.w() * p2.x() - p1.x() * p2.w())
    r.setW(-p1.x() * p2.y() + p1.y() * p2.x())

    norm = np.sqrt(r.x() * r.x() + r.y() * r.y() - r.w() * r.w())
    if norm == 0.0:
        raise DivisionByZero("weierstrassCrossProduct : possible divide by zero error")

    r.setX(r.x() / norm)
    r.setY(r.y() / norm)
    r.setW(r.w() / norm)
    return r


# TODO: Abstract Classes?
class Element:
    """
    An Element is a set of Points which define some geometry. One or more Elements
    together make up a pattern. Element is not designed to be used on it's own.
    Use on of the derived classes instead.
    """

    def __init__(self):
        self._points = []
        self._cid = 0
        self._filled = False
        self._open = False
        self._type = ElemType.ELEMENT
        self._id = 0  # #TODO: some kind of IdFactory.
        self._zorder = 1
        self._lineStyle = LineStyle.SOLID

    def filled(self) -> bool:
        """Return whether the element is filled.

        Returns:
            bool: filled or not.
        """
        return not self.open() & self._filled

    def open(self) -> bool:
        """Return whether the element is open.

        Returns:
            bool: Open or not.
        """
        return self._open

    def cid(self) -> int:
        """Return the color id of the element.

        Returns:
            int: color id.
        """
        return self._cid

    def numPoints(self) -> int:
        """Return the number of points in the element.

        Returns:
            int: number of points
        """
        return len(self._points)

    def getPoint(self, i: int) -> Point:
        """Return the point at index i.

        Args:
            i (int): index of point

        Returns:
            Point: Point at index i.
        """
        return self._points[i]

    def type(self) -> ElemType:
        """Return the type of the element.

        Returns:
            ElemType: Type of Element
        """
        return self._type

    def id(self) -> int:
        """Return the id of the element.

        Returns:
            int: id of element
        """
        return self._id

    def zorder(self) -> int:
        """Return the z-order of the element.

        Returns:
            int: z-order of element
        """
        return self._zorder

    def lineStyle(self) -> LineStyle:
        """Return the line style of the element.

        Returns:
            LineStyle: Line style of element.
        """
        return self._lineStyle

    def transform(self, tran: Transformation):
        """Transform the element.

        Args:
            tran (Transformation): Transformation to apply.
        """
        for p in self._points:
            p.transform(tran)
        # change elements's color to one suggested by
        # the color permutation
        self.setCid(tran.colorPerm()[self.cid()])

    def setCid(self, cid: int):
        """Set the color id of the element.

        Args:
            cid (int): Color id.
        """
        self._cid = cid

    def addPoint(self, p: Point):
        """Add a point to the element.

        Args:
            p (Point): Point to add.
        """
        self._points.append(p)

    def setFilled(self, f: bool):
        """Set whether the element is filled.

        Args:
            f (bool): Filled or not.
        """
        self._filled = f

    def setZOrder(self, z: int):
        """Set the z-order of the element.

        Args:
            z (int): z-order
        """
        self._zorder = z

    def setLineStyle(self, ls: LineStyle):
        """Set the line style of the element.

        Args:
            ls (LineStyle): The line style.
        """
        self._lineStyle = ls

    def clone(self):
        """Make a copy of the element.

        Returns:
            Element: The copied element.
        """
        e = copy.deepcopy(self)
        e._id = 0  # TODO: some kind of IdFactory.
        return e


class EuclidPolyLine(Element):
    """EuclidPolyLine is a line in euclidean space."""

    def __init__(self):
        super().__init__()
        self._open = True
        self._type = ElemType.EUCLID_POLYLINE


class EuclidPoly(Element):
    """EuclidPoly is a polygon in euclidean space."""

    def __init__(self):
        super().__init__()
        self._open = False
        self._type = ElemType.EUCLID_POLY


class Circle(Element):
    """Circle is a circle in euclidean space."""

    def __init__(self):
        super().__init__()
        self._open = False
        self._type = ElemType.CIRCLE


# /**


class HyperLine:
    """
    Helper class for Hyperbolic figures. Almost all hyperbolic figures like
    hyperpolyline and hyperpoly need hyperlines to construct themselves.

    Note: This class is NOT derived from Element. So to actually construct a hyperline
    use HyperPolyLine with 2 points.
    """

    def __init__(self) -> None:
        self._startPoint = Point()
        self._endPoint = Point()
        self._topLeft = Point()
        self._startAngle = 0.0
        self._endAngle = 0.0
        self._width = 0.0
        self._height = 0.0
        self._shouldDrawArc = False

    def setPoints(self, p1: Point, p2: Point):
        """Set the points of the hyperline.

        Args:
            p1 (Point): Start point.
            p2 (Point): End point.
        """
        self._startPoint = p1
        self._endPoint = p2
        # Ensure start and end points are in Poincare Coordinates
        self._startPoint.weierstrassToPoincare()
        self._endPoint.weierstrassToPoincare()

        p1.poincareToWeierstrass()
        p2.poincareToWeierstrass()

        a = weierstrassCrossProduct(p1, p2)

        if np.abs(a.w()) < 1e-6:
            # If this curve is too flat, better to approximate with straight line
            self._shouldDrawArc = False
            return

        self._shouldDrawArc = True
        xc = a.x() / a.w()
        yc = a.y() / a.w()

        # Vector to end points of the arc from the center
        u1, v1, u2, v2 = (
            self._startPoint.x() - xc,
            self._startPoint.y() - yc,
            self._endPoint.x() - xc,
            self._endPoint.y() - yc,
        )
        r = np.sqrt(u1**2 + v1**2)

        # This make sure that the arc is drawn in the anti-clockwise direction
        theta = np.arctan2((v2 * u1 - v1 * u2), (u1 * u2 + v1 * v2))

        self._startAngle = np.atan2(v1, u1) * 180 / np.pi
        self._endAngle = theta * 180 / np.pi

        self._topLeft.setX(xc - r)
        self._topLeft.setY(yc + r)
        self._width = 2 * r
        self._height = 2 * r

    def topLeft(self) -> Point:
        """Return the top left point of the hyperline.

        Returns:
            Point: top left point.
        """
        return self._topLeft

    def width(self):
        """Return the width of the hyperline.

        Returns:
            int: Width
        """
        return self._width

    def height(self):
        """Return the height of the hyperline.

        Returns:
            int: Height
        """
        return self._height

    def startAngle(self) -> float:
        """Return the start angle of the hyperline.

        Returns:
            float: Start Angle.
        """
        return self._startAngle

    def endAngle(self) -> float:
        """Return the end angle of the hyperline.

        Returns:
            float: End angle
        """
        return self._endAngle

    def startPoint(self) -> Point:
        """Return the start point of the hyperline.

        Returns:
            Point: Start point.
        """
        return self._startPoint

    def endPoint(self) -> Point:
        """Return the end point of the hyperline.

        Returns:
            Point: End point.
        """
        return self._endPoint

    def shouldDrawArc(self) -> bool:
        """Return whether the hyperline should be drawn as an arc.

        Returns:
            bool: Draw arc or not.
        """
        return self._shouldDrawArc


class HyperPolyLine(Element):
    """
    After adding all the points, use hyperLines() to get the parameters for drawing
    hyperlines.
    """

    def __init__(self):
        super().__init__()
        self._open = True
        self._type = ElemType.HYPER_POLYLINE
        self._lines = []

    def addPoint(self, p: Point):
        """Add a point to the hyperpolyline.

        Args:
            p (Point): Point to add.
        """
        super().addPoint(p)

        count = self.numPoints()
        if count >= 2:
            hline = HyperLine()
            # create a hyperline from last point to current pt
            hline.setPoints(self.getPoint(count - 2), self.getPoint(count - 1))
            # add it to the lines store.
            self._lines.append(hline)

    def hyperLines(self) -> list:
        """Return the hyperlines of the hyperpolyline.

        Returns:
            list: Lines
        """
        return self._lines

    def transform(self, tran: Transformation):
        """Rebuild hyperlines

        Args:
            tran (Transformation): Transformation to apply.

        Raises:
            InvalidCodepoint: Incomplete hyperpolyline.
        """
        super().transform(tran)
        # remove old lines
        self._lines.clear()
        if self.numPoints() < 2:
            # TODO: Code this error
            raise InvalidCodepoint(
                "HyperPolyLine::transform : "
                "Cannot transform an incomplete Hyper polyline"
            )
        # rebuild lines
        for i in range(self.numPoints()):
            hline = HyperLine()
            hline.setPoints(self.getPoint(i - 1), self.getPoint(i))
            self._lines.append(hline)


class HyperPoly(HyperPolyLine):
    """HyperPoly is a polygon in hyperbolic space."""

    def __init__(self):
        super().__init__()
        self._open = False
        self.type = ElemType.HYPER_POLY
        self._id = 0  # IdFactory.getUid()

    def addPoint(self, p: Point):
        """Add a point to the hyperpoly.

        Args:
            p (Point): Point to add.
        """
        super().addPoint(p)
        count = self.numPoints()
        # 4 or more points exist (including the new point)
        if count > 3:
            # remove last added hyperline
            self._lines.pop()
            hline = HyperLine()
            # hline from last point to new point
            hline.setPoints(self.getPoint(count - 2), self.getPoint(self.count - 1))
            # add it to the lines store.
            self._lines.append(hline)
            # hline from new point to first point
            hline.setPoints(self.getPoint(count - 1), self.getPoint(0))
            # add it to the lines store.
            self._lines.append(hline)
        elif count == 3:
            hline = HyperLine()
            # hline from last point to new point
            hline.setPoints(self.getPoint(count - 2), self.getPoint(self.count - 1))
            # add it to the lines store.
            self._lines.append(hline)
            # hline from new point to first point
            hline.setPoints(self.getPoint(count - 1), self.getPoint(0))
            # add it to the lines store.
            self._lines.append(hline)
        # only two points so far, just add a hyperline
        elif count == 2:
            hline = HyperLine()
            # hline from last point to new point
            hline.setPoints(self.getPoint(count - 2), self.getPoint(count - 1))
            # add it to the lines store.
            self._lines.append(hline)

    def transform(self, tran: Transformation):
        """Transform the hyperpolygon.

        Args:
            tran (Transformation): Transformation to apply.
        """
        super().transform(tran)
        # join last point to first
        hline = HyperLine()
        # hline from last point to new point
        hline.setPoints(
            self.getPoint(self.numPoints() - 1), self.getPoint(self.numPoints() - 0)
        )
        # add it to the lines store.
        self._lines.append(hline)
