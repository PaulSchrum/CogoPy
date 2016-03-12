from unittest import TestCase
import Coordinates.vector as vector
from Coordinates.vector import Vector as Vector


class TestVector(TestCase):
    def test_createVectorNoParams(self):
        vec = Vector()
        self.assertAlmostEqual(vec.dX, 0.0, 5)
        self.assertAlmostEqual(vec.dY, 0.0, 5)
        self.assertIsNone(vec.dZ)

    def test_create2Dvector(self):
        vec = Vector(1,1)
        self.assertAlmostEqual(vec.dX, 1.0, 5)
        self.assertAlmostEqual(vec.dY, 1.0, 5)
        self.assertIsNone(vec.dZ)

    def test_create3Dvector(self):
        vec = Vector(1,1,7)
        self.assertAlmostEqual(vec.dX, 1.0, 5)
        self.assertAlmostEqual(vec.dY, 1.0, 5)
        self.assertAlmostEqual(vec.dZ, 7.0, 5)
