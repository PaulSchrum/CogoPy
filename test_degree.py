from unittest import TestCase
from degree import *
import degree
import math

class TestDegree(TestCase):
    def test_asRadiansDouble(self):
        deg = Degree(45.0)
        self.assertTrue(deg.asRadiansFloat() == math.pi / 4.0)

    def test_asDegreesDouble(self):
        deg = Degree(45.0)
        self.assertTrue(deg.asDegreesFloat() == 45.0)

    def test_factoryFromRadians(self):
        deg = Degree.factoryFromRadians(math.pi / 2.0)
        self.assertTrue(deg.asDegreesFloat() == 90.0)

    def test_DegreesConstructorFromDMS(self):
        deg = Degree(12, 34, 56.7)
        actual = deg.asDegreesFloat()
        expected = 12.582416666667
        self.assertAlmostEqual(actual, expected, 5)
        deg = Degree(-12, 34, 56.7)
        actual = deg.asDegreesFloat()
        expected = -12.582416666667
        self.assertAlmostEqual(actual, expected, 5)

    def test_factory_decimalDegrees(self):
        deg = Degree.factory(12.0)
        self.assertTrue(deg.asDegreesFloat() == 12.0)

    def test_factory_DMS(self):
        deg = Degree.factory(12, 30, 30)
        actual = deg.asDegreesFloat()
        expected = 12.5 + 30.0 / 3600.0
        self.assertAlmostEqual(actual, expected, 5)
        deg = Degree.factory(-12, 30, 30)
        actual = deg.asDegreesFloat()
        expected *= -1.0
        self.assertAlmostEqual(actual, expected, 5)

    def test_getDegreesAsDMS(self):
        deg = Degree(2, 3, 4 + 2.0/3.0)
        actual = deg.asDegreesFloat()
        expected = 2.05129629631
        self.assertAlmostEqual(actual, expected, 8)
        actual = deg.asDMS()
        expected = (2, 3, 4 + 2.0/3.0)
        self.assertEqual(expected[0],actual[0])
        self.assertEqual(expected[1],actual[1])
        self.assertAlmostEqual(actual[2], expected[2], 5)

        deg = Degree(-2, 3, 4 + 2.0/3.0)
        actual = deg.asDMS()
        expected = (-2, 3, 4 + 2.0/3.0)
        self.assertEqual(expected[0],actual[0])
        self.assertEqual(expected[1],actual[1])
        self.assertAlmostEqual(actual[2], expected[2], 5)

    def test_getDegreesAsDMSstring(self):
        deg = Degree(12, 3, 4)
        expected = '12' + degree.degree_sign + " 3' "+  '4.0"'
        actual = deg.asDMSstring()
        self.assertEqual(expected, actual)

        deg = Degree(-12, 3, 4)
        expected = '-12' + degree.degree_sign + " 3' "+  '4.0"'
        actual = deg.asDMSstring()
        # print 'expected:', expected
        # print '  actual:', actual
        self.assertEqual(expected, actual)
