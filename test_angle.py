from unittest import TestCase
from angle import *
import math
import mock

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


