# ==============================================================================================
# This file contains utility classes and functionality relating to the functionality performed
# by companion agents in these missions. This includes things such as additional math functionality, 
# planning, and small algorithms that are meant to be reused.
# ==============================================================================================
import math
from collections import namedtuple

# ==============================================================================================
# Named tuples
# ==============================================================================================

Vector = namedtuple("Vector", "x y z")    # Vector/Position holding x, y, and z values
EntityInfo = namedtuple("EntityInfo", "id type position quantity")   # Information for an entity observed by an agent
Action = namedtuple("Action", "type args")
RecipeItem = namedtuple("RecipeItem", "type quantity")

# ==============================================================================================
# Classes
# ==============================================================================================

class MathExt:
    """
    An extension of the math module to support vector operations and calculations within tolerance.
    """

    PI_OVER_TWO = math.pi / 2
    THREE_PI_OVER_TWO = 3 * math.pi / 2
    TWO_PI = math.pi * 2

    @staticmethod
    def valuesAreEqual(a, b, tol = 0):
        """
        Returns true if two numeric values are equal. Optionally supply a tolerance.
        """
        diff = a - b
        if diff < 0:
            diff = diff * -1
        if diff <= tol:
            return True
        else:
            return False

    @staticmethod
    def affineTransformation(value, x, y, a, b):
        """
        Transform a value from the range [x, y] to the range [a, b] and return it.
        """
        return (value - x) * (b - a) / (y - x) + a

    @staticmethod
    def distanceBetweenPoints(pointA, pointB):
        """
        Returns the distance between two points, where each point is specified as a named Vector.
        """
        return math.sqrt(math.pow(pointB.x - pointA.x, 2) + math.pow(pointB.y - pointA.y, 2) + math.pow(pointB.z - pointA.z, 2))

    @staticmethod
    def vectorFromPoints(pointA, pointB):
        """
        Returns a Vector from point A to point B.
        """
        return Vector(pointB.x - pointA.x, pointB.y - pointA.y, pointB.z - pointA.z)

    @staticmethod
    def vectorMagnitude(vector):
        """
        Returns the magnitude of a 'Vector'.
        """
        return math.sqrt(vector.x * vector.x + vector.y * vector.y + vector.z * vector.z)

    @staticmethod
    def normalizeVector(vector):
        """
        Normalize a Vector into the range (-1, -1, -1) to (1, 1, 1) and return it.
        If the given Vector is the zero vector, returns the zero vector.
        """
        mag = MathExt.vectorMagnitude(vector)
        if MathExt.valuesAreEqual(mag, 0, 1.0e-14):
            return Vector(0, 0, 0)
        else:
            return Vector(vector.x / mag, vector.y / mag, vector.z / mag)

    @staticmethod
    def dotProduct(vectorA, vectorB):
        """
        Returns the dot product of a Vector with another Vector.
        """
        return vectorA.x * vectorB.x + vectorA.y * vectorB.y + vectorA.z * vectorB.z

    @staticmethod
    def isZeroVector(vector):
        """
        Returns true if the Vector given is equal to the zero vector.
        """
        if vector.x == 0 and vector.y == 0 and vector.z == 0:
            return True
        return False