from unittest import TestCase
from Angles.azimuth import Azimuth
from degree import Degree
from _helpers import nearlyEqual

class TestAzimuth(TestCase):
    def test_createAzimuthNoParams(self):
        newAz = Azimuth()
        self.assertTrue(not newAz is None)
        self.assertTrue(nearlyEqual(newAz._angle,0.0))

    def test_createAzimuthFromFloat(self):
        newAz = Azimuth(1.0)
        self.assertTrue(nearlyEqual(newAz._angle, 1.0))

    def test_createAzimuthFromDegree(self):
        newAz = Azimuth(Degree(45.0))
        self.assertTrue(nearlyEqual(newAz.asRadians(), 0.7853981634))