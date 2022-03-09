# //
# // C++ Interface: irregularpgon
# //
# // Description:
# //
# //
# // Author: Ajit Datar <ajitdatar@gmail.com>, (C) 2005
# //
# // Copyright: See COPYING file that comes with this distribution
# //
# //
# #ifndef IRREGULARPGON_H
# #define IRREGULARPGON_H

import numpy as np

from .defs import DiagramType
from .diagram import Diagram
from .pattern import Pattern
from .pgonedge import PgonEdge
from .transformation import Transformation

# /**
# A diagram using irregular pgons. This class implements an algorithm with pgon vertex
# at the center.

# @author Ajit Datar
# */


class IrregularPgon(Diagram):
    """_summary_"""

    def __init__(self):
        """_summary_"""
        super().__init__()
        self._q = np.array([], dtype=np.int)
        self.edgeTran = np.array([], dtype=np.int)
        self.cosP_i = np.array([], dtype=np.int)
        self._pgonPat = Pattern()

    def init(self):
        """_summary_"""
        self.initTrans()

    def clear(self):
        """_summary_"""
        super().clear()
        self._q = np.array([], dtype=np.int)
        self.edgeTran = np.array([])
        self._pgonPat = np.array([])

    def make(self):
        pass

    def type(self) -> DiagramType:
        return DiagramType.IRREGULAR_PGON

    def setP(self, v: int):
        super().setP(v)
        self._q.resize(v, refcheck=False)

    def setQ(self, vertex: int, val: int):
        self._q[vertex] = val

    def initTrans(self):
        """_summary_"""
        q_sum = self._q.sum()
        avg_q = (q_sum / self._p) + 1
        self.cosP_i.resize(self._p, refcheck=False)
        # TODO: Vectorize this:
        for i in range(self._p):
            self.cosP_i[i] = np.cos(np.pi / self._q[i])
        x = np.sin(np.pi / self._p) / np.cos(np.pi / avg_q)
        x_old = x - self.F(x) / self.FPrime(x)
        while abs(x - x_old) > 1e-10:
            x_old = x
            x = x - self.F(x) / self.FPrime(x)

        for i in range(2):  # why is this 2?
            x = x - self.F(x) / self.FPrime(x)

        coshEby2 = 1 / x  # cosh(E/2)
        sinhEby2 = np.sqrt(coshEby2 * coshEby2 - 1)
        self.coshE = 2 * coshEby2 * coshEby2 - 1
        self.sinhE = 2 * coshEby2 * sinhEby2
        # This is by no means NOT DONE!

    def initFrame(self, x: float, moveTran: Transformation):
        pass

    def F(self, x: float) -> float:
        return 0.0

    def FPrime(self, x: float) -> float:
        return 1.0


# class IrregularPgon : public Diagram
# {
# public:
#     IrregularPgon();

#     virtual ~IrregularPgon();
#     virtual void init() { initTrans(); }
#     virtual void clear();
#     virtual void make();
#     //get methods
#     virtual DiagramType type() { return IRREGULAR_PGON; }
#     //set methods
#     virtual void setP(int v);
#     virtual void setQ(int vertex, int val) { q_[vertex] = val; }
# protected: //methods
#     void makeHelper(Exposure exposure, int layerId, Transformation& tran);
#     Transformation shiftTran(const Transformation& tran, int shift);
#     /**
#     Initialize transformations required for this diagram.
#     edgeTran transformations are used by drawing algo.
#     */
#     void initTrans();
#     /**initializes the frame for the fundamental pattern */
#     void initFrame(double x, Transformation& moveTran);
# protected: //data
#     vector<int> q_;
#     vector<Transformation> edgeTran;

#     vector<double> cosP_i; //cosines of angles at a vertex
#     Pattern pgonPat_;
# private:
#     double F(double x); //F(x) for newton's method
#     double FPrime(double x); //F'(x) for newton's method
# };

# #endif
