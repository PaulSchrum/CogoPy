'''
Azimuth Class
Represents a compass direction.
Inherits from Angle.
Values are constrainsed to be between 0 and 2pi radians
(that is, value, v, is contstained so that 0.0 <= v < 360.0)
Value 0.0 is due north.
Value 45.0 is north-east.
Value 90.0 is due east.
Value 180.0 is due south.
Value 270.0 is due west.
'''
from angle import Angle
from degree import Degree

degree_sign= u'\N{DEGREE SIGN}'

class Azimuth(Angle):
    def __init__(self, inputParam=None):
        if inputParam is None:
            self._angle = 0.0
            return

        print type(inputParam)
        if isinstance(inputParam, float):
            self._angle = inputParam
        if isinstance(inputParam, Degree):
            self._angle = inputParam.asRadiansFloat()

    def __repr__(self):
        return "{0}{1}".format(self.asDegreesFloat(),degree_sign)
