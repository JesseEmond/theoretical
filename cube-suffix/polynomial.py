"""Representation of a polynomial f(x) = c[n]*x^n + ... + c[1]*x + c[0]."""

class Polynomial:

    def __init__(self, coefficients):
        """Represents f(x) = c[n]*x^n + ... + c[1]*x  + c[0]."""
        assert len(coefficients) > 0
        self.coefficients = coefficients

    def eval(self, x):
        """Evaluates f(x)."""
        xs = [x**i for i in range(len(self.coefficients))]
        terms = [coefficient * x
                 for coefficient, x in zip(self.coefficients, xs)]
        return sum(terms)

    def derivative(self):
        """Returns f'(x)."""
        # d(a*x^n)/dx = a*n*x^(n-1), c[0] disappears, the rest "shifts left".
        coefficients = [coefficient * i
                        for i, coefficient in enumerate(self.coefficients)]
        return Polynomial(coefficients[1:])
