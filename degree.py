'''

'''
import math

degree_sign= u'\N{DEGREE SIGN}'

class Degree:
    '''
    Makes a float value have units of Degrees (1/360th of a circle).
    '''
    def __init__(self, newValue, minutes=None, seconds=None):
        self._degrees = float(newValue)
        _sign = math.copysign(1.0, self._degrees)
        if minutes is not None:
            self._degrees += _sign * float(minutes) / 60.0
            if seconds is not None:
                self._degrees += _sign * float(seconds) / 3600.0


    def asRadiansFloat(self):
        return self._degrees * math.pi / 180.0

    def asDegreesFloat(self):
        return self._degrees

    def asDMS(self):
        """
        :return: self as a Tuple of (Degrees, Minutes, Seconds)
                Degrees is int. Minutes is int. Seconds is Float.
        """
        sign_ = math.copysign(1, self._degrees)
        absVal = math.modf(math.fabs(self._degrees))
        integerPart = absVal[1]
        x = math.modf(absVal[0] * 60.0)
        minutes = int(x[1])
        seconds = x[0] * 60.0
        return (int(sign_ * integerPart), minutes, seconds)

    def asDMSstring(self):
        """
        :return: string in the form of degrees minutes seconds.
        """
        tupl_ = self.asDMS()
        return str(tupl_[0]) + degree_sign + ''' {0}' {1}"'''.format(tupl_[1], tupl_[2])


    @staticmethod
    def factoryFromRadians(radians):
        return Degree(180.0 * radians / math.pi)

    @staticmethod
    def factory(deg, minutes=None, seconds = None):
        return Degree(deg, minutes, seconds)

