'''

'''
import math


class Degree:
    def __init__(self, newValue):
        self._degrees = newValue

    def asRadiansDouble(self):
        return self._degrees * math.pi / 180.0

    def asDegreesDouble(self):
        return self._degrees

    @staticmethod
    def factoryFromRadians(radians):
        return Degree(180.0 * radians / math.pi)

    @staticmethod
    def factory(deg, minutes=None, seconds = None):
        if minutes is None:
            return Degree(deg)

        return Degree(deg +
                      minutes / 60.0 +
                      seconds / 3600.0)

