from unittest import TestCase
from point import *

class TestPoint(TestCase):
    def test_2DpointCreation_NoParams(self):
        newPt = Point()
        self.assertTrue(newPt.X == 0.0)
        self.assertTrue(newPt.Y == 0.0)
        self.assertTrue(newPt.Z is None)

    def test_2DpointCreateion(self):
        newPt = Point(1, 2)
        self.assertTrue(newPt.X == 1.0)
        self.assertTrue(newPt.Y == 2.0)
        self.assertTrue(newPt.Z is None)

    def test_3DpointCreateion(self):
        newPt = Point(1, 2, 3)
        self.assertTrue(newPt.X == 1.0)
        self.assertTrue(newPt.Y == 2.0)
        self.assertFalse(newPt.Z is None)
        self.assertTrue((newPt.Z == 3.0))

