"""Vector"""

import math as m

__author__ = "Askar Takhirov"

class Vector:
    def __init__(self, x:float=0.0, y:float=0.0): #I couldnt figure out how to pass test 1 without doing this
        self._x = x
        self._y = y

    # Getters and setters
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x:float):
        self._x = x

    def set_y(self, y:float):
        self._y = y

    # String representation for testing purposes
    def __str__(self):
        return f"<{self._x}, {self._y}>"

    def __repr__(self):
        return f"Vector x = {self._x}, y = {self._y})"

    # Equality check
    def __eq__(self, other):
        return isinstance(other, Vector) and self._x == other.get_x() and self._y == other.get_y()

    def __ne__(self, other):
        return not self.__eq__(other)

    # Vector addition
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self._x + other.get_x(), self._y + other.get_y())
        raise TypeError("Operand must be a Vector")

    # Vector subtraction
    def __sub__(self, other):
        if isinstance(other, Vector):
            return Vector(self._x - other.get_x(), self._y - other.get_y())
        raise TypeError("Operand must be a Vector")

    # Scalar multiplication (times)
    def times(self, scalar:float):
        if isinstance(scalar, (int, float)):
            return Vector(self._x * scalar, self._y * scalar)
        raise TypeError("Operand must be a scalar (int or float)")

    # Distance between two vectors
    def distance_to(self, other):
        if isinstance(other, Vector):
            dx = self._x - other.get_x()
            dy = self._y - other.get_y()
            return m.sqrt(dx ** 2 + dy ** 2)
        raise TypeError("Operand must be a Vector")