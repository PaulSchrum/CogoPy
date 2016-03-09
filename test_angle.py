from unittest import TestCase
from angle import *
from degree import Degree
import degree
import math
import mock
from _helpers import *

class TestAngle(TestCase):
    def test_twoPi(self):
        self.assertTrue(twoPi == math.pi * 2.0)

    def test_init(self):
        a = Angle(twoPi / 8.0)
        degDbl = a.asDegreesFloat()
        self.assertTrue(degDbl == 45.0)

    def test_factory_passIn_xAndy(self):
        a = Angle.factory(10.0, 10.0)
        degDbl = a.asDegreesFloat()
        self.assertTrue(degDbl == 45.0)

    def test_factory_passInDuckPoints(self):
        p1 = mock.MagicMock()
        p1.X = 1.0
        p1.Y = 1.0
        p2 = mock.MagicMock()
        p2.X = 10.0
        p2.Y = 10.0
        a = Angle.factory(p1, p2)
        degDbl = a.asDegreesFloat()
        self.assertTrue(degDbl == 45.0)

    def test_inputAnglesOutsideNorms(self):
        angle1 = Angle.factory(Degree(45.0))
        self.assertTrue(nearlyEqual(angle1.asDegreesFloat(), 45.0))

        angle1 = Angle.factory(Degree(180.0))
        self.assertTrue(nearlyEqual(angle1.asDegreesFloat(), 180.0))

        angle1 = Angle.factory(Degree(190.0))
        deg = angle1.asDegreesFloat()
        self.assertTrue(nearlyEqual(angle1.asDegreesFloat(), -170.0))

        angle1 = Angle.factory(Degree(350.0))
        self.assertTrue(nearlyEqual(angle1.asDegreesFloat(), -10.0))

        angle1 = Angle.factory(Degree(370.0))
        self.assertTrue(nearlyEqual(angle1.asDegreesFloat(), 10.0))

        angle1 = Angle.factory(Degree(710.0))
        self.assertTrue(nearlyEqual(angle1.asDegreesFloat(), -10.0))

        angle1 = Angle.factory(Degree(-710.0))
        self.assertTrue(nearlyEqual(angle1.asDegreesFloat(), 10.0))

    def test_getAsDMS(self):
        angl_ = Angle(Degree(10,3,5))
        expected = (10, 3, 5.0)
        actual = angl_.asDMS()
        self.assertEqual(expected[0],actual[0])
        self.assertEqual(expected[1],actual[1])
        self.assertAlmostEqual(actual[2], expected[2], 5)

    def test_getAsDMSstring(self):
        deg = Angle(Degree(16,30,24))
        expected = '16' + degree.degree_sign + " 30' "+  '24.0"'
        actual = deg.asDMSstring()
        self.assertEqual(expected, actual)

