'''
Class to represent an angle.  It hides the overhead
of converting between radians and other representations
of angle, providing wrappers for the basic trig
functions.
'''
import math

twoPi = 2 * math.pi
piOver2 = math.pi / 2.0

def RadiansToDegreesDouble(radians):
    return 180.0 * radians / math.pi

class Angle:
    def __init__(self, doubleValue = 0.0):
        self._angle = doubleValue

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

    def asDegreesDouble(self):
        return RadiansToDegreesDouble(self._angle)

    def sin(self):
        return math.sin(self._angle)

    def cos(self):
        return math.cos(self._angle)

    def tan(self):
        return math.tan(self._angle)
