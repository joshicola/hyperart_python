import numpy as np


class Permutation:
    def __init__(self, perm=None):
        if perm is None:
            self.perm = np.zeros(0, dtype=int)
            self._size = 0
        else:
            self.perm = perm.copy()
            self._size = perm.size()

    def setSize(self, size):
        self.perm = np.zeros(size, dtype=int)
        self._size = size

    def initIdentity(self):
        pass

    def __getitem__(self, key):
        return self.perm[key]

    def __setitem__(self, key, item):
        self.perm[key] = item

    # TODO: Copy constructor??

    def __iadd__(self, other):
        pass

    def __lshift__(self, other):
        pass

    def __add__(self, other):
        pass


# How to do class operators in python?
#     Permutation(const Permutation&);    //copy constructor
#     Permutation& operator=(const Permutation&); //copy assignment
#     size_t size() const { return size_; }
#     size_t& operator[](const size_t i);
#     const size_t& operator[](const size_t i) const;
#     Permutation& operator+=(const Permutation& perm);
#     friend ostream& operator<< (ostream& o, const Permutation& perm);
# private:
#     size_t size_;
#     PermIndexVec_ vec_;
# };

# const Permutation operator+(const Permutation& p1, const Permutation& p2);
