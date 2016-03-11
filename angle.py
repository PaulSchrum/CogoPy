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
        self.valu = val

    @property
    def valu(self):
        return self._angle

    @valu.setter
    def valu(self, val):
        if val is None:
            self._angle = 0.0
        elif isinstance(val, float):
            self._angle = val
        elif isinstance(val, int):
            self._angle = float(val)
        else:
            self._angle = val.asRadiansFloat()
        self._normalize()


    def _normalize(self):
        self._angle = math.atan2(math.sin(self._angle), math.cos(self._angle))


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
        return self.valu

    def asDegreesFloat(self):
        return RadiansToDegreesFloat(self.valu)

    def asDMS(self):
        retDeg = Degree.factoryFromRadians(self.valu)
        return retDeg.asDMS()

    def asDMSstring(self):
        retDeg = Degree.factoryFromRadians(self.valu)
        return retDeg.asDMSstring()

    def sin(self):
        return math.sin(self.valu)

    def cos(self):
        return math.cos(self.valu)

    def tan(self):
        return math.tan(self.valu)

