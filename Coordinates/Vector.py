


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

