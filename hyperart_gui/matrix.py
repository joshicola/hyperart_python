import numpy as np


# TODO: Replace this throughout with numpy matrices
class Matrix:
    """Class for matrix multiplication"""

    def __init__(self, rows=3, columns=3) -> None:
        self._rows = rows
        self._columns = columns
        self._matrix = np.matrix(np.zeros((rows, columns)))

    def rows(self) -> int:
        """Return number of rows in matrix

        Returns:
            int: Matrix rows
        """
        return self._rows

    def cols(self) -> int:
        """Return number of columns in matrix

        Returns:
            int: Matrix columns
        """
        return self._columns

    def initIdent(self):
        """Initialise matrix to identity matrix"""
        self._matrix = np.matrix(np.zeros((self._rows, self._columns)))
        if self.rows < self._columns:
            self._matrix[: self._rows, : self._rows] = np.identity(self._rows)
        else:
            self._matrix[: self._columns, : self._columns] = np.identity(self._columns)

    def reinit(self, rows=3, columns=3):
        """Reinitialise matrix to new dimensions with zero values"""
        self._rows = rows
        self._columns = columns
        self._matrix = np.matrix(np.zeros((rows, columns)))

    def __iadd__(self, other):
        """Add (+) operator

        Args:
            other (Matrix): Matrix to add to self

        Returns:
            Matrix: Result of addition
        """
        self._matrix += other._matrix
        return self

    def __mul__(self, other):
        """Multiply (*) operator

        Args:
            other (Matrix): Matrix to multiply to self

        Returns:
            Matrix: Result of multiplication
        """
        new_matrix = Matrix(self._rows, other._columns)
        new_matrix._matrix = self._matrix * other._matrix
        return new_matrix
