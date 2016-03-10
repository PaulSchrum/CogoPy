from unittest import TestCase

from Angles.deflection import Deflection
from degree import Degree

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


