from unittest import TestCase

from Angles.deflection import Deflection
from degree import Degree
from Angles.azimuth import Azimuth as Azimuth

class TestDeflection(TestCase):
    def test_Deflection_basicCreation(self):
        defl = Deflection(Degree(7.0))
        self.assertIsNotNone(defl)
        expected = 7.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        defl = Deflection(Degree(359.0))
        expected = 359.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        defl = Deflection(Degree(361.0))
        expected = 1.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        defl = Deflection(Degree(-21.0))
        expected = -21.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        defl = Deflection(Degree(-361.0))
        expected = -1.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

    def test_createDeflectionBySubtractingTwoAzimuths(self):
        az1 = Azimuth(Degree(10.0))
        az2 = Azimuth(Degree(350.0))
        defl = az2 - az1
        expected = -20.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)
        az3 = az1 + defl
        self.assertAlmostEqual(az2.valu, az3.valu, 5)
        deflComplement = defl.complement360()
        expected = 340.0
        actual = deflComplement.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        defl = az1 - az2
        expected = 20.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)
        az3 = az2 + defl
        self.assertAlmostEqual(az1.valu, az3.valu, 5)
        deflComplement = defl.complement360()
        expected = -340.0
        actual = deflComplement.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

    def test_deflectionGreaterThanPiComplementsToLTpi(self):
        defl = Deflection(Degree(350.0))
        defl = defl.complement360()
        expected = -10.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        defl = Deflection(Degree(-345.0))
        self.assertAlmostEqual(defl.asDegreesFloat(), -345.0, 5)
        defl = defl.complement360()
        expected = 15.0
        actual = defl.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)
