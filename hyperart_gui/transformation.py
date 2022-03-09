"""/***************************************************************************
 *   Copyright (C) 2005 by Dr. Douglas Dunham, Ajit Datar                  *
 *   ddunham@d.umn.edu , data0003@d.umn.edu                                *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                  *
 *                                                                         *
 ***************************************************************************/
"""
from .defs import (
    DiagramType,
    ElemType,
    Exposure,
    LineStyle,
    Orientation,
    PanType,
    ViewMode,
    ZoomType,
)
from .matrix import Matrix
from .permutation import Permutation


class Transformation:
    """
    A transformation consists of matrix, color permutations etc
    """

    def __init__(self, ncolors=3):
        self._matrix = 0  # matrix
        self._permutation = 0  # permutation
        self._color_permutation = 0  # color_permutation
        self._orientation = 0  # orientation

    def matrix(self) -> Matrix:
        return self._matrix

    def colorPermutation(self) -> Permutation:
        return self._color_permutation

    def pPos(self) -> int:
        return self._ppos

    def orient(self) -> Orientation:
        return self._orientation

    def initIdentity(self):
        pass

    def setMatrix(self, matrix: Matrix):
        self._matrix = matrix

    def setColorPermutation(self, permutation: Permutation):
        self._color_permutation = permutation

    def setpPos(self, ppos: int):
        self._ppos = ppos

    def setOrient(self, orient: Orientation):
        self._orientation = orient

    def __imul__(self, other):
        """
        Add two transformations
        """
        pass


# @author Ajit Datar
# */
# class Transformation
# {
# public:
#     Transformation(int ncolors = 3);

#     Matrix &matrix() { return mat_; }
#     const Matrix &matrix() const { return mat_; }
#     Permutation &colorPerm() { return colorPerm_; }
#     const Permutation &colorPerm() const { return colorPerm_; }
#     int pPos() const { return pPos_; }
#     Orientation orient() const { return orient_; }
#     void initIdentity();

#     void setMatrix(Matrix m) { mat_ = m; }
#     void setColorPerm(Permutation p) { colorPerm_ = p; }
#     void setpPos(int val) { pPos_ = val; }
#     void setOrient(Orientation o) { orient_ = o; }
#     Transformation &operator*=(const Transformation &t);

#     ~Transformation();


# private:
#     Matrix mat_;
#     Permutation colorPerm_;
#     int pPos_; // TODO does it matter for anything else but edgeTran?
#     Orientation orient_;
# };

# const Transformation operator*(const Transformation &t1, const Transformation &t2);

# #endif
