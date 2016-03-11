'''
Deflection is an Angle intended to be used in angle arithmatic.
Deflection is a change in direction.  Plus is to the right.
Horizontal Cogo items all have a Deflection value.
'''

from angle import *
# import azimuth

class Deflection(Angle):
    '''
    Deflection is constrained to be +/- 1 Turn (+/- 2pi)
    '''

    def _normalize(self):
        sign_ = math.copysign(1.0, self._angle)
        self._angle /= 2.0
        super(Deflection, self)._normalize()
        self._angle *= 2.0
        if sign_ > 0.0:
            if self._angle < 0.0:
                self._angle += 2.0 * math.pi
            elif self._angle > 2.0*math.pi:
                self._angle -= 2.0 * math.pi
        elif sign_ < 0.0:
            if self._angle < -2.0*math.pi:
                self._angle += 2.0*math.pi
            elif self._angle > 0.0:
                self._angle -= 2.0*math.pi

# Todo: get Deflection addition to work. Problem is circular imports
    # def __add__(self, azmuth):
    #     if "<class 'azimuth.Azimuth'>" == str(type(azmuth)):
    #         newAz = self.valu + azmuth.valu
    #         return azimuth.Azimuth(newAz)
    #     else:
    #         raise NotImplementedError("Addition operation not supported for Deflection plus Angle or its children.  Use Deflection + Azimuth.")



