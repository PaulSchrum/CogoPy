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

    def test_inputAnglesOutsideNorms(self):
        az1 = Azimuth(Degree(40.0))
        self.assertAlmostEqual(az1.asDegreesFloat(),40.0, 5)

        az1 = Azimuth(Degree(270.0))
        self.assertAlmostEqual(az1.asDegreesFloat(),270.0, 5)

        az1 = Azimuth(Degree(-10.0))
        deg = az1.asDegreesFloat()
        self.assertAlmostEqual(deg,350.0, 5)

        az1 = Azimuth(Degree(370.0))
        deg = az1.asDegreesFloat()
        self.assertAlmostEqual(deg,10.0, 5)

