'''
Basic point class.  X, Y, and Z are properties.
Z will be None for 2D points.
'''
from iBoundingBoxed import IBoundingBoxed
from boundingBox import BoundingBox

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
        return self.distanceTo(other) < equalityTolerance
