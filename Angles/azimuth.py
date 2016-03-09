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
from angle import Angle, RadiansToDegreesFloat
from degree import Degree
import math

degree_sign= u'\N{DEGREE SIGN}'

class Azimuth(Angle):
    """
    :param doubleValue: float (interpreted as Radians) or Degree
    :return: new instance of Azimuth
    """
    def __init__(self, inputParam):
        if inputParam is None:
            self.__angle = 0.0
        elif isinstance(inputParam, float):
            self.__angle = inputParam
        else:
            self.__angle = inputParam.asRadiansFloat()
        self._normalize()

    @property
    def _angle(self):
        return self._getAsAzimuth()

    @_angle.setter
    def angle(self, val):
        if isinstance(val, float):
            self.__angle = val
        else:
            self.__angle = val.asRadiansFloat()
        self._normalize()

    def _normalize(self):
        """
        Convert self.__angle from Angle to Azimuth.
        Recommend that client code not call this method.
        :Note: Upon entry __angle is interpreted as Angle (-pi -- pi), 0 is due east.
            Upon exit __angle is interpreted as Azimuth (0 -- 2pi), 0 is due north.
        :return: None
        """
        __angle = (math.pi / 2.0) - self.__angle
        __angle = math.atan2(math.sin(__angle), math.cos(__angle))
        self.__angle = (math.pi / 2.0) - __angle
        if self.__angle < 0.0:
            self.__angle += 2.0 * math.pi

    def _getAsAzimuth(self):
        # retVal = (math.pi / 2.0) - self.__angle
        return self.__angle

    def asDegreesFloat(self):
        degRad = RadiansToDegreesFloat(self._angle)
        return degRad

    @property
    def __repr__(self):
        return "{0}{1}".format(self.asDegreesFloat(),degree_sign)
