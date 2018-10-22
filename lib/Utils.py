# ==============================================================================================
# This file contains utility classes and functionality relating to the functionality performed
# by companion agents in these missions. This includes things such as additional math functionality, 
# planning, and small algorithms that are meant to be reused.
# ==============================================================================================
import math

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
        Returns the distance between two points.
        """
        return math.sqrt(math.pow(pointB[0] - pointA[0], 2) + math.pow(pointB[1] - pointA[1], 2) + math.pow(pointB[2] - pointA[2], 2))

    @staticmethod
    def vectorFromPoints(pointA, pointB):
        """
        Returns an (x, y, z) vector from point A to point B.
        """
        return (pointB[0] - pointA[0], pointB[1] - pointA[1], pointB[2] - pointA[2])

    @staticmethod
    def vectorMagnitude(vector):
        """
        Returns the magnitude of a vector.
        """
        return math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])

    @staticmethod
    def normalizeVector(vector):
        """
        Normalize a vector into the range (-1, -1, -1) to (1, 1, 1) and return it.
        If the given vector is the zero vector, returns the zero vector.
        """
        mag = MathExt.vectorMagnitude(vector)
        if MathExt.valuesAreEqual(mag, 0, 1.0e-14):
            return (0, 0, 0)
        else:
            return (vector[0] / mag, vector[1] / mag, vector[2] / mag)

    @staticmethod
    def dotProduct(vectorA, vectorB):
        """
        Returns the dot product of two vectors.
        """
        return vectorA[0] * vectorB[0] + vectorA[1] * vectorB[1] + vectorA[2] * vectorB[2]

    @staticmethod
    def isZeroVector(vector):
        """
        Returns true if the vector given is equal to the zero vector.
        """
        if vector[0] == 0 and vector[1] == 0 and vector[2] == 0:
            return True
        return False