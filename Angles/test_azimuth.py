from unittest import TestCase
from Angles.azimuth import Azimuth
from degree import Degree
import Angles.deflection
from _helpers import nearlyEqual

class TestAzimuth(TestCase):
    def test_createAzimuthNoParams(self):
        newAz = Azimuth()
        self.assertTrue(not newAz is None)
        self.assertTrue(nearlyEqual(newAz.valu, 0.0))

    def test_createAzimuthFromFloat(self):
        newAz = Azimuth(1.0)
        self.assertTrue(nearlyEqual(newAz.valu, 1.0))

    def test_createAzimuthFromDegree(self):
        newAz = Azimuth(Degree(45.0))
        self.assertTrue(nearlyEqual(newAz.asRadians(), 0.7853981634))
        newAz = Azimuth(Degree(356.0))
        expected = 6.2133721371
        actual = newAz.valu
        self.assertAlmostEqual(expected, actual, 7)

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

    def test_TrigFunctionsForAzimuth(self):
        az1 = Azimuth(Degree(10.0))
        expected = 0.984807753012
        actual = az1.sin()
        self.assertAlmostEqual(expected, actual, 5)

        actual = az1.cos()
        expected = 0.173648177667
        self.assertAlmostEqual(expected, actual, 5)

        actual = az1.tan()
        expected = 5.67128181962
        self.assertAlmostEqual(expected, actual, 5)

    def test_AzimuthAddition_Deflection(self):
        az = Azimuth(Degree(2.5))
        defl = Angles.deflection.Deflection(Degree(3.5))
        newAz = az + defl
        expected = 6.0
        actual = newAz.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        defl = Angles.deflection.Deflection(Degree(-12.0))
        newAz = newAz + defl
        expected = 360.0 - 6.0
        actual = newAz.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        az = Azimuth(Degree(355.0))
        defl = Angles.deflection.Deflection(Degree(12.5))
        newAz = az + defl
        expected = 7.5
        actual = newAz.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        az = Azimuth(Degree(356))
        expected = 6.2133721371
        actual = az.valu
        self.assertAlmostEqual(expected, actual, 7)
        defl = Angles.deflection.Deflection(Degree(-352.0))
        newAz = az + defl
        expected = 4.0
        actual = newAz.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        az = Azimuth(Degree(1)) + Angles.deflection.Deflection(Degree(-90))
        expected = 271.0
        actual = az.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        az = Azimuth(0) + Angles.deflection.Deflection(Degree(-90))
        expected = 270.0
        actual = az.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

    # def test_Deflection_AdditionAzimuth(self):
    #     az = Azimuth(0)
    #     defl = Deflection(Degree(-90))
    #     newAz = defl + az
    #     expected = 270.0
    #     actual = newAz.asDegreesFloat()
    #     self.assertAlmostEqual(expected, actual, 5)




