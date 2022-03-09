import numpy as np


# TODO: Replace this throughout with numpy matrices
class Matrix:
    def __init__(self, rows=3, columns=3) -> None:
        self._rows = rows
        self._columns = columns
        self._matrix = np.matrix(np.zeros((rows, columns)))

    def rows(self) -> int:
        return self._rows

    def cols(self) -> int:
        return self._columns

    def initIdent(self):
        self._matrix = np.matrix(np.zeros((self._rows, self._columns)))
        if self.rows < self._columns:
            self._matrix[: self._rows, : self._rows] = np.identity(self._rows)
        else:
            self._matrix[: self._columns, : self._columns] = np.identity(self._columns)

    def reinit(self, rows=3, columns=3):
        self._rows = rows
        self._columns = columns
        self._matrix = np.matrix(np.zeros((rows, columns)))

    def __iadd__(self, other):
        self._matrix += other._matrix
        return self

    def __mul__(self, other):
        new_matrix = Matrix(self._rows, other._columns)
        new_matrix._matrix = self._matrix * other._matrix
        return new_matrix


# /**
# A matrix of double-precision numbers
# Always stored row-major
# eg A 3x4 matrix has 3 rows and 4 columns

# Reinterpretation of matrix size to different row X col value
# is not supported (you can do that by deriving your own class from this)
# @author Ajit Datar
# */
# class Matrix
# {
# public:
#     /**
#     Creates a matrix of size r X c and initializes all elements to 0.
#     Default is to create a 3x3 matrix.
#     */
#     Matrix(int r = 3, int c = 3);
#     int rows() const { return rows_; }
#     int cols() const { return cols_; }
#     /**
#     Makes this matrix an identity matrix
#     */
#     void initIdentity();

#     /**
#     resizes the matrix to r x c
#     Old matrix data is lost
#     */
#     void reinit(int r = 3, int c = 3);
#     /**
#     get a reference to the row vector

#     Even though this is against the OO practice of data hiding,
#     this is provided so that we can use a natural notation like matrix[i][j]
#     to directly get/set elements.
#     Susceptible to overflow errors.
#     */
#     vector<double> &operator[](int r) { return storage_[r]; }
#     const vector<double> &operator[](int r) const { return storage_[r]; }

#     Matrix &operator+=(const Matrix &m);

#     ~Matrix();

# protected:
#     int rows_;
#     int cols_;
#     vector<vector <double> > storage_; // internal storage for matrix elements
# };

# /**
# Matrix multiplication m1 * m2

# */
# const Matrix operator*(const Matrix &m1, const Matrix &m2);

# ostream &operator<<(ostream &o, const Matrix &m);

# #endif
