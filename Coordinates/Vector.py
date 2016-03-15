import math
from Angles.azimuth import Azimuth
import degree
import Angles.deflection as dfl

class Vector(object):
    def __init__(self, DX=0.0, DY=0.0, DZ=None):
        self.dX = float(DX)
        self.dY = float(DY)
        if DZ is None:
            self.dZ = DZ
        else:
            self.dZ = float(DZ)

    @property
    def dX(self):
        return self._dx

    @dX.setter
    def dX(self, val):
        self._dx = val

    @property
    def dY(self):
        return self._dy

    @dY.setter
    def dY(self, val):
        self._dy = val

    @property
    def dZ(self):
        return self._dz

    @dZ.setter
    def dZ(self, val):
        self._dz = val

    def _getMagnitude(self):
        if self.dZ is None:
            dz = 0.0
        else:
            dz = self.dZ
        return math.sqrt(self.dX ** 2.0 + self.dY ** 2.0 + dz ** 2.0)

    @property
    def magnitude(self):
        return self._getMagnitude()

    @magnitude.setter
    def magnitude(self, val):
        if not isinstance(val, float) and not isinstance(val, int):
            raise TypeError("Magnitude must be of type 'float' or 'int'.")
        ratio = val / self._getMagnitude()
        self.scaleBy(ratio)

    def scaleBy(self, scaleFactor, yScale=None, zScale=None):
        self.dX *= scaleFactor
        if yScale is not None:
            self.dY *= yScale
        else:
            self.dY *= scaleFactor

        if self.dZ is not None:
            if zScale is not None:
                self.dZ *= zScale
            else:
                self.dZ *= scaleFactor

    @property
    def azimuth(self):
        az = Azimuth()
        az.valu = math.atan2(self.dX, self.dY)
        return az

    @azimuth.setter
    def azimuth(self, val):
        magXYplane = math.sqrt(self.dX ** 2.0 + self.dY ** 2.0)
        if isinstance(val, Azimuth):
            self.dX = magXYplane * val.cos()
            self.dY = magXYplane * val.sin()
        elif isinstance(val, degree.Degree):
            newVal = Azimuth(val)
            self.dX = magXYplane * newVal.cos()
            self.dY = magXYplane * newVal.sin()
        else:
            raise TypeError("azimuth can only be set from an instance of Azimuth.")

    def __add__(self, other):
        if isinstance(other, Vector):
            newDX = self.dX + other.dX
            newDY = self.dY + other.dY
            if self.dZ is None:
                if other.dZ is None:
                    newDZ = None
                else:
                    newDZ = other.dZ
            else:
                if other.dZ is None:
                    newDZ = self.dZ
                else:
                    newDZ = self.dZ + other.dZ
            return Vector(newDX, newDY, newDZ)
        elif isinstance(other, dfl.Deflection):
            returnVec = Vector(self.dX, self.dY, self.dZ)
            returnVec.azimuth = returnVec.azimuth + other
            return returnVec

    def spinInXYbyTurns(self, turns):
        """rotates the current Vector in the XY plane (ie, about the Z axis)
        the number of turns specified. For example, spinInXYbyTurns(-0.25)
        spins the Vector 90 degrees to the left (Azimuth convention) of the original."""
        defl = dfl.Deflection(degree.Degree(360.0 * turns))
        self.azimuth = self.azimuth + defl
