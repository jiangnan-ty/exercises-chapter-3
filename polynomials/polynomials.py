from numbers import Number
from numbers import Integral


class Polynomial:

    def __init__(self, coefs):
        l = list(i for i, e in enumerate(coefs) if e != 0)
        if l:
            self.coefficients = coefs[0:max(l)+1]
        else:
            self.coefficients = (0,)

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a - b for a, b in
                          zip(self.coefficients, other.coefficients))
            if self.degree() >= other.degree():
                coefs += self.coefficients[common:]
            else:
                coefs += tuple(a*-1 for a in other.coefficients[common:])
            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other, )
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __rsub__(self, other):
        return Polynomial((0, )) - (self - other)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Polynomial(tuple(other*a for a in self.coefficients))

        elif isinstance(other, Polynomial):
            order = self.degree() + other.degree()
            coefs = list(0 for j in range(order+1))
            for i in range(order+1):
                _term = 0
                if i <= self.degree():
                    for j in range(i, max(i-other.degree(), 0)-1, -1):
                        _term += self.coefficients[j] * other.coefficients[i-j]
                else:
                    for j in range(self.degree(),
                                   max(0, (i-other.degree()))-1, -1):
                        _term += self.coefficients[j] * other.coefficients[i-j]
                coefs[i] = _term
            return Polynomial(tuple(coefs))

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):
        if isinstance(other, Integral):
            _c = Polynomial((1,))
            count = 0
            while count < other:
                _c *= self
                count += 1
            return _c
        else:
            return NotImplemented

    def __call__(self, arg):
        deg = self.degree()
        c = 0
        for i in range(deg+1):
            c += self.coefficients[i]*arg**i
        return c

    def dx(self):
        if self.degree() != 0:
            return Polynomial(tuple(_i*_e for _i, _e in
                                    enumerate(self.coefficients) if _i))
        else:
            return Polynomial((0,))


def derivative(arg):
    return Polynomial.dx(arg)
