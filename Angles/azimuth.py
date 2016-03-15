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
+ deflections are clockwise.
- deflections are counterclockwise
'''
from angle import Angle, RadiansToDegreesFloat
from degree import Degree
import math
from deflection import Deflection as Deflection

degree_sign= u'\N{DEGREE SIGN}'

class Azimuth(Angle):
    """
    :param doubleValue: float (interpreted as Radians) or Degree
    :return: new instance of Azimuth
    """
    # Todo: Accept or return Azimuths a Degree-Minutes-Seconds
    # Todo: Accept or return Azimuths as Bearings (DMS)

    @Angle.valu.getter
    def valu(self):
        return self._getAsAzimuth()

    def _normalize(self):
        """
        Convert self._angle from Angle to Azimuth.
        Recommend that client code not call this method.
        :Note: Upon entry _angle is interpreted as Angle (-pi -- pi), 0 is due east.
            Upon exit _angle is interpreted as Azimuth (0 -- 2pi), 0 is due north.
        :return: None
        """
        __angle = (math.pi / 2.0) - self._angle
        __angle = math.atan2(math.sin(__angle), math.cos(__angle))
        self._angle = (math.pi / 2.0) - __angle
        if self._angle < 0.0:
            self._angle += 2.0 * math.pi

    def _getAsAzimuth(self):
        # retVal = (math.pi / 2.0) - self._angle
        return self._angle

    def asAngleFloat(self):
        """
        :return: value in Angle range (-pi -- pi) but of type Double
        """
        retAngle = (math.pi / 2.0) - self.valu
        if retAngle > math.pi:
            retAngle = (2.0 * math.pi) - retAngle
        elif retAngle < -math.pi:
            retAngle = (2.0 * math.pi) + retAngle
        return retAngle

    def asAngle(self):
        retAngle = (math.pi / 2.0) - self.valu
        return Angle(retAngle)

    def asDegreesFloat(self):
        degRad = RadiansToDegreesFloat(self.valu)
        return degRad

    @property
    def _floatDegrees(self):
        return RadiansToDegreesFloat(self.valu)

    def __add__(self, deflction):
        if isinstance(deflction, Deflection):
            newAz = self.valu + deflction.valu
            return Azimuth(newAz)
        else:
            raise TypeError("Addition operation not supported for Azimuth plus Angle or its children.  Use Azimuth + Deflection.")

    def __sub__(self, other):
        """
        Returns a deflection of the difference between the two Azimuths.
        Note: This always returns the interior solution to the deflection.
        If you need the exterior solution, call complement360() on the Deflection.
        Example: defl = (Az2 - Az1).complement360()
        :param other: Azimuth
        :return: Deflection (will always be +/- pi)
        """
        if isinstance(other, Azimuth):
            v1 = self.valu
            v2 = other.valu
            diff = v2 - v1
            if diff < -math.pi:
                diff += 2.0 * math.pi
                diff *= -1.0
            elif diff > math.pi:
                diff -= 2.0 * math.pi
                diff *= -1.0
            return Deflection(diff)
        else:
            raise TypeError()

    def sin(self):
        """
        :return: Sine of the Azimuth (float) as if it were Angle
        """
        return math.sin(self.asAngleFloat())

    def cos(self):
        """
        :return: Cosine of the Azimuth (float) as if it were Angle
        """
        return math.cos(self.asAngleFloat())

    def tan(self):
        """
        :return: Tangent of the Azimuth (float) as if it were Angle
        """
        return math.tan(self.asAngleFloat())

    @property
    def __repr__(self):
        return "{0}{1}".format(self.asDegreesFloat(),degree_sign)
