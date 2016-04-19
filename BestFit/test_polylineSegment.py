from unittest import TestCase
from PolylineSegment import PolylineSegment
from ExtendedPoint import ExtendedPoint

somePoints = [
    ExtendedPoint(11,13),
    ExtendedPoint(15,19),
    ExtendedPoint(19.5,19.5)
]

class TestPolylineSegment(TestCase):
    def test_polylineSegment_createdCorrectly(self):
        newPLS = PolylineSegment(somePoints)
        self.assertEqual(first=3,second=len(newPLS))
        expected = ExtendedPoint(15.0, 19.0)
        self.assertTrue(expected == newPLS[1])
