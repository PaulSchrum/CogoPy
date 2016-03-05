'''
Basic point class.  X, Y, and Z are properties.
Z will be None for 2D points.
'''

class Point:
    '''
    Represents a Point in 2D or 3D space.
    Property X: X coordinate (or Easting)
    Property Y: Y coordinate (or Northing)
    Property Z: Z coordinate (or elevation)
    ToDo: Later implementations will provide aliases for
        these values for Long, Lat, and Elevation
    '''

    def __init__(self, x=0.0, y=0.0, z=None):
        self.X = x
        self.Y = y
        self.Z = z

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

