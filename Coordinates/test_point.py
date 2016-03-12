from unittest import TestCase
from math import fabs
import Coordinates.point as point
from _helpers import nearlyEqual

_tol = 6

class TestPoint(TestCase):
    def test_2DpointCreation_NoParams(self):
        newPt = point.Point()
        self.assertTrue(newPt.X == 0.0)
        self.assertTrue(newPt.Y == 0.0)
        self.assertTrue(newPt.Z is None)

    def test_2DpointCreateion(self):
        newPt = point.Point(1, 2)
        self.assertTrue(newPt.X == 1.0)
        self.assertTrue(newPt.Y == 2.0)
        self.assertTrue(newPt.Z is None)

    def test_3DpointCreateion(self):
        newPt = point.Point(1, 2, 3)
        self.assertTrue(newPt.X == 1.0)
        self.assertTrue(newPt.Y == 2.0)
        self.assertFalse(newPt.Z is None)
        self.assertTrue((newPt.Z == 3.0))

    def test_PointToPointDistanceComputation(self):
        tol = 0.000005
        pt1 = point.Point(2,2)
        pt2 = point.Point(3,3)
        pt3 = point.Point(4,4,4)
        pt4 = point.Point(5,5,5)
        d1_2 = pt1.distanceTo(pt2)
        d3_4 = pt3.distanceTo(pt4)
        d1_3 = pt1.distanceTo(pt3)
        self.assertAlmostEqual(1.41421356, d1_2, _tol)
        self.assertAlmostEqual(1.73205080757, d3_4, _tol)
        self.assertAlmostEqual(4.89897949, d1_3, _tol)

    def test_2DBoundingBox(self):
        newPt = point.Point(5,6)
        bb = newPt.getBoundingBox()
        self.assertTrue(bb.LowerLeft == point.Point(5,6))
        self.assertTrue(bb.UpperRight == point.Point(5,6))

