'''
Basic point class.  X, Y, and Z are properties.
Z will be None for 2D points.
'''
from iBoundingBoxed import IBoundingBoxed
from boundingBox import BoundingBox
from Coordinates.vector import Vector as Vector
from _helpers import nearlyEqual

#equalityTolerance - for comparing floats within the point
equalityTolerance = 0.00005

class Point(IBoundingBoxed):
    '''
    Represents a Point in 2D or 3D space.
    Property X: X coordinate (or Easting)
    Property Y: Y coordinate (or Northing)
    Property Z: Z coordinate (or elevation)
    ToDo: Later implementations will provide aliases for
        these values for Long, Lat, and Elevation
    '''

    def __init__(self, x=0.0, y=0.0, z=None):
        self.X = float(x)
        self.Y = float(y)
        if z is None:
            self.Z = z
        else:
            self.Z = float(z)

    @property
    def X(self):
        return self.__x

    @X.setter
    def X(self, val):
        self.__x = val

    @property
    def Y(self):
        return self.__y

    @Y.setter
    def Y(self, val):
        self.__y = val

    @property
    def Z(self):
        return self.__z

    @Z.setter
    def Z(self, val):
        self.__z = val

    def getBoundingBox(self):
        retBB = BoundingBox(self)
        return retBB

    def distanceTo(self, other):
        assert isinstance(other, Point)
        dx2 = (other.X - self.X)**2.0
        dy2 = (other.Y - self.Y)**2.0
        oZ = other.Z
        if oZ is None:
            oZ = 0.0
        sZ = self.Z
        if sZ is None:
            sZ = 0.0
        dz2 = (oZ - sZ)**2.0
        return (dx2 + dy2 + dz2)**0.5

    def __eq__(self, other):
        return nearlyEqual(self.distanceTo(other), 0.0, equalityTolerance)
        # return self.distanceTo(other) < equalityTolerance

    def __ne__(self, other):
        return not self.__eq__(other)

    def assertPointEqual(self, other, tolerance=equalityTolerance):
        if not nearlyEqual(self.distanceTo(other), 0.0, tolerance):
            raise AssertionError("Two points are not equal.")

    def __add__(self, other):
        if isinstance(other, Vector):
            newX = self.X + other.dX
            newY = self.Y + other.dY
            newZ = self.Z
            if not newZ is None:
                if not other.dZ is None:
                    newZ += other.dZ
            return Point(newX, newY, newZ)
        else:
            raise TypeError("Point can only add to type Vector")

    def __radd__(self, other):
        if isinstance(other, Vector):
            self.X = self.X + other.dX
            self.Y = self.Y + other.dY
            if self.Z is None:
                if not other.dZ is None:
                    self.Z = other.dZ
            else:
                if not other.dZ is None:
                    self.Z = self.Z + other.dZ
        else:
            raise TypeError("Point can only add to type Vector")

