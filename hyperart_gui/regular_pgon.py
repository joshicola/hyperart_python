# /***************************************************************************
#  *   Copyright (C) 2005 by Ajit Datar, Dr. Douglas Dunham   *
#  *   ajitdatar@gmail.com, ddunham@d.umn.edu   *
#  *                                                                         *
#  *   This program is free software; you can redistribute it and/or modify  *
#  *   it under the terms of the GNU General Public License as published by  *
#  *   the Free Software Foundation; either version 2 of the License, or     *
#  *   (at your option) any later version.                                   *
#  *                                                                         *
#  *   This program is distributed in the hope that it will be useful,       *
#  *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#  *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#  *   GNU General Public License for more details.                          *
#  *                                                                         *
#  *   You should have received a copy of the GNU General Public License     *
#  *   along with this program; if not, write to the                         *
#  *   Free Software Foundation, Inc.,                                       *
#  *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
#  ***************************************************************************/

from .defs import DiagramType, Exposure, ReflSymType
from .diagram import Diagram
from .permutation import Permutation
from .transformation import Transformation

# /**
# A diagram which is based on regular pgons. This constitute the original Escher circle
# limit I-IV patterns.

# @author Ajit Datar
# */


class RegularPgon(Diagram):
    """
    _summary_
    """

    def __init__(self):
        """ """
        # TODO: Check this.
        super().__init__()
        self._q = []
        self._pgonPat = 0
        self._fundRegEdges = 0
        self._reflSym = 0
        self._reflColorPerm = Permutation()
        self._rotnColorPerm = Permutation()
        self._x2pt, self._xqpt, self._yqpt = 0, 0, 0
        self.reflectHypot, self.reflectPgonEdge, self.reflectEdgeBisector = 0, 0, 0
        self.rot2 = 0
        self.rotp, self.rotpInv = [], []
        self.edgeTran = []

        self._edge_ = 0
        self._reflSym = 0

    def init(self):
        pass

    def clear(self):
        pass

    def make(self):
        pass

    def type(self) -> DiagramType:
        return DiagramType.REGULAR_PGON

    def reflSym(self) -> ReflSymType:
        return self._reflSym

    def reflColorPerm(self) -> Permutation:
        return self._reflColorPerm

    def rotnColorPerm(self) -> Permutation:
        return self._rotnColorPerm

    def fundRegEdges(self) -> int:
        return self._fundRegEdges

    def setQ(self, v: int):
        self._q = v

    def setReflSym(self, v: ReflSymType):
        self._reflSym = v

    def setNumColors(self, v: int):
        self._numColors = v
        self._rotnColorPerm.setSize(self.numColors())
        self._reflColorPerm.setSize(self.numColors())

    def setFundRegEdges(self, v: int):
        self._fundRegEdges = v

    def makePgonPat(self):
        pass

    def makeHelper(self, exposure: Exposure, layerId: int, tran: Transformation):
        pass

    def shiftTran(self, tran: Transformation, shift: int) -> Transformation:
        pass

    def initTrans(self):
        pass
