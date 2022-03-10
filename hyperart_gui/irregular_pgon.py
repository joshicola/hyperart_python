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

from .defs import DiagramType, Exposure
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
        # pgonPat_.clear();

        # QMap<PatId, PatternPtr>::iterator it;
        # for(it=diag_.begin(); it != diag_.end(); ++it) {
        #     delete it.data();
        # }
        # diag_.clear();
        # for(unsigned int i=0; i<layers_.size(); i++) {
        #     layers_[i].clear();
        # }
        # animq.clear();
        # layers_.resize(numLayers_);

        # pgonPat_ = *(fundPat().clone()); //copy existing set of elements (this will remove the old set)
        # addPattern(0, pgonPat_);

        # if(numLayers_ > 1) {
        #     Transformation qtran = edgeTran[0];
        #     for(int i=0; i< q_[0]; i++) {
        #         makeHelper(MAXEXPOSURE, 1, qtran);
        #         if( (-1 % p_) != 0) {
        #             qtran = shiftTran(qtran, -1);
        #         }
        #     }
        # }

    def type(self) -> DiagramType:
        return DiagramType.IRREGULAR_PGON

    def setP(self, v: int):
        super().setP(v)
        self._q.resize(v, refcheck=False)

    def setQ(self, vertex: int, val: int):
        self._q[vertex] = val

    def makeHelper(self, exposure: Exposure, layerId: int, tran: Transformation):
        pass
        # ParametersIRP param(p_);

        # PatternPtr pat = pgonPat_.cloneAndTransform(tran);
        # addPattern(layerId, *pat);
        # if(layerId < numLayers_ -1) {
        #     int pskip = param.pSkip(exposure);
        #     int verticesTodo = param.verticesTodo(exposure);
        #     for(int i=0; i< verticesTodo; i++) {
        #         //setptran
        #         Transformation ptran = shiftTran(tran, pskip);
        #         Transformation qtran(numColors());
        #         //set qtran based on ptran
        #         int qskip = param.qSkip(exposure,i);
        #         if( (qskip % p_) != 0) {
        #             qtran = shiftTran(ptran, qskip);
        #         }
        #         else {
        #             qtran = ptran;
        #         }
        #         int vert = (ROTATION == ptran.orient()) ? ((ptran.pPos()-1 + p_) % p_) : ptran.pPos();
        #         int pgonsTodo = q_[vert] - param.pgonsToSkip(exposure, i);
        #         for(int j=0; j<pgonsTodo; j++) {
        #             if( (3 == p_) && ( j == (pgonsTodo-1))) {
        #                 pat = pgonPat_.cloneAndTransform(qtran);
        #                 addPattern(layerId+1, *pat);
        #             }
        #             else {
        #                 makeHelper(param.exposure(layerId, i, j), layerId+1, qtran);
        #             }
        #             if( (-1 % p_) != 0) {
        #                 qtran = shiftTran(qtran, -1);
        #             } //else don't change qtran
        #         }
        #         pskip = (pskip +1)% p_;
        #     }
        # }

    def shiftTran(self, tran: Transformation, shift: int) -> Transformation:
        pass
        # int newEdge = (tran.pPos() + tran.orient() * shift + 2*p_) % p_;
        # if(newEdge < 0 || newEdge > (p_-1)) {
        #     throw "RegularPgon::shiftTran newEdge out of range";
        # }
        # return tran * edgeTran[newEdge];

    def initTrans(self):
        """_summary_"""
        q_sum = self._q.sum()
        avg_q = (q_sum / self._p) + 1
        self.cosP_i.resize(self._p, refcheck=False)  # I might not need this
        self.cosP_i = np.cos(np.pi / self._q)
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
        # Transformation reflectEdgeBisector(numColors());
        # {
        #     Matrix& mat = reflectEdgeBisector.matrix();
        #     mat[1][1] = -1.0;
        #     reflectEdgeBisector.setOrient(REFLECTION);
        # }

        # Transformation reflectPgonEdge(numColors());
        # {
        #     Matrix& mat = reflectPgonEdge.matrix();
        #     mat[0][0] = -coshE;
        #     mat[0][2] = sinhE;
        #     mat[2][0] = -sinhE;
        #     mat[2][2] = coshE;
        # }

        # Transformation rot2 = reflectPgonEdge * reflectEdgeBisector;

        # Transformation moveLeft(numColors()), moveLeftInv(numColors());
        # {
        #     Matrix& mat = moveLeft.matrix();
        #     mat[0][0] = coshEby2;
        #     mat[0][2] = -sinhEby2;
        #     mat[2][0] = -sinhEby2;
        #     mat[2][2] = coshEby2;
        # }
        # {
        #     Matrix& mat = moveLeftInv.matrix();
        #     mat[0][0] = coshEby2;
        #     mat[0][2] = sinhEby2;
        #     mat[2][0] = sinhEby2;
        #     mat[2][2] = coshEby2;
        # }

        # double centerAngle = asin(x*cosP_i[0]);
        # double coshHypot = (cos(centerAngle)/sin(centerAngle)) * (cos(PI/q_[0])/sin(PI/q_[0]));
        # double sinhHypot = sqrt(coshHypot*coshHypot - 1);
        # Point down;
        # down.setX(sinhHypot * cos(centerAngle));
        # down.setY(sinhHypot * sin(centerAngle));
        # down.setW(coshHypot);
        # down.setType("weierstrass");
        # down.transform(moveLeft);

        # Transformation moveDown(numColors()), moveDownInv(numColors());
        # {
        #     Matrix& mat = moveDown.matrix();
        #     mat[1][1] = down.w();
        #     mat[1][2] = -down.y();
        #     mat[2][1] = -down.y();
        #     mat[2][2] = down.w();
        # }
        # {
        #     Matrix& mat = moveDownInv.matrix();
        #     mat[1][1] = down.w();
        #     mat[1][2] = down.y();
        #     mat[2][1] = down.y();
        #     mat[2][2] = down.w();
        # }

        # Transformation moveTran = moveDown * moveLeft;
        # Transformation moveTranInv = moveLeftInv * moveDownInv;

        # vector<Transformation> rotp(p_), rotpInv(p_);
        # Permutation identity(numColors());
        # double ang = 0;
        # for(int i=0; i<p_; i++) {
        #     {
        #         rotp[i].initIdentity();
        #         rotp[i].setColorPerm(identity);
        #         Matrix& mat = rotp[i].matrix();
        #         mat[0][0] = cos( ang );
        #         mat[0][1] = -sin( ang );
        #         mat[1][0] = sin( ang );
        #         mat[1][1] = cos( ang );
        #     }

        #     {
        #         rotpInv[i].initIdentity();
        #         rotpInv[i].setColorPerm(identity);
        #         Matrix& mat = rotpInv[i].matrix();
        #         mat[0][0] = cos( ang );
        #         mat[0][1] = sin( ang );
        #         mat[1][0] = -sin( ang );
        #         mat[1][1] = cos( ang );
        #     }
        #     ang += 2 * asin(x*cosP_i[i]);
        # }

        # edgeTran.resize(p_);
        # for(int i=0; i<p_; i++) {
        #     int adjEdge = edges[i].adjEdgeId();
        #     if(REFLECTION == edges[i].orientation()) {
        #         edgeTran[i] = moveTran * rotp[i] * reflectPgonEdge * rotpInv[adjEdge] * moveTranInv;
        #     }
        #     else if(ROTATION == edges[i].orientation() ) {
        #         edgeTran[i] = moveTran * rotp[i] * rot2 * rotpInv[adjEdge] * moveTranInv;
        #     }
        #     else {
        #         throw "Error: invalid orientation";
        #     }
        #     edgeTran[i].setOrient(edges[adjEdge].orientation());
        #     edgeTran[i].setpPos(adjEdge);
        #     edgeTran[i].setColorPerm(edges[i].colorPerm());
        # }
        # initFrame(x,moveTran);

    def initFrame(self, x: float, moveTran: Transformation):
        pass
        # double baseAng = 0.0;
        # HyperPoly *hpol = new HyperPoly();

        # for(int i=0; i<p_; i++) {
        #     double ang = asin(x*cosP_i[i]);
        #     double coshHypot = (cos(ang)/sin(ang)) * (cos(PI/q_[i])/sin(PI/q_[i]));
        #     double sinhHypot = sqrt(coshHypot*coshHypot - 1);
        #     double u = sinhHypot * cos(baseAng + ang)/(coshHypot+1);
        #     double v = sinhHypot * sin(baseAng + ang)/(coshHypot+1);
        #     Point p(u,v);
        #     cerr<<u<<","<<v<<endl;
        #     p.poincareToWeierstrass();
        #     p.transform(moveTran);
        #     hpol->addPoint(p);
        #     baseAng += 2 * ang;
        # }

        # //hpol->addPoint(hpol->getPoint(0));
        # hpol->setZOrder(10000);
        # hpol->setCid(0);
        # hpol->setFilled(false);
        # fundPat_.addElement(hpol, true, true);

    def F(self, x: float) -> float:
        """_summary_

        Args:
            x (float): _description_

        Returns:
            float: _description_
        """
        result = np.sum(np.arcsin(x * self.cosP_i)) - np.pi
        return result

    def FPrime(self, x: float) -> float:
        """_summary_

        Args:
            x (float): _description_

        Returns:
            float: _description_
        """
        result = np.sum(self.cosP_i / np.sqrt(1 - (x * self.cosP_i) ** 2))
        return result


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
