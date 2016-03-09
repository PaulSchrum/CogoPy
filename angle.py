'''
Class to represent an angle.  It hides the overhead
of converting between radians and other representations
of angle, providing wrappers for the basic trig
functions.
'''
import math
from degree import Degree

twoPi = 2 * math.pi
piOver2 = math.pi / 2.0

def RadiansToDegreesFloat(radians):
    return 180.0 * radians / math.pi

class Angle(object):
    def __init__(self, val = 0.0):
        '''
        :param doubleValue: float (interpreted as Radians) or Degree
        :return: new instance of Angle
        '''
        if isinstance(val, float):
            self.__angle = val
        else:
            self.__angle = val.asRadiansFloat()
        self._normalize()

    @property
    def _angle(self):
        return self.__angle

    @_angle.setter
    def _angle(self, val):
        self.__angle = val
        self._normalize()


    def _normalize(self):
        self.__angle = math.atan2(math.sin(self.__angle), math.cos(self.__angle))


    @staticmethod
    def factory(a, b=None):
        if b is None:
            return Angle(a)

        dx = a
        dy = b
        if (hasattr(a, 'X') and hasattr(a,'Y') and
            hasattr(b,'X') and hasattr(b, 'Y')):
            dx = b.X - a.X
            dy = b.Y - a.Y

        return Angle(math.atan2(dy, dx))

    def asRadians(self):
        return self._angle

    def asDegreesFloat(self):
        return RadiansToDegreesFloat(self._angle)

    def sin(self):
        return math.sin(self._angle)

    def cos(self):
        return math.cos(self._angle)

    def tan(self):
        return math.tan(self._angle)

