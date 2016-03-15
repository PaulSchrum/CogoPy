from unittest import TestCase
import Coordinates.vector as vector
from Coordinates.vector import Vector as Vector
from Coordinates.point import Point as Point
from Angles.deflection import Deflection as Deflection
import math
import degree

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

    def test_VectorAddition_Vector_makesNewVector(self):
        v1 = Vector(1,2)
        v2 = Vector(3,4)
        vResult = v1 + v2
        self.assertIsNotNone(vResult)
        self.assertIsInstance(vResult, Vector)
        self.assertAlmostEqual(vResult.dX, 4.0, 5)
        self.assertAlmostEqual(vResult.dY, 6.0, 5)
        self.assertIsNone(vResult.dZ)

        v1 = Vector(1,2, 3)
        v2 = Vector(3,4)
        vResult = v1 + v2
        self.assertIsNotNone(vResult)
        self.assertIsInstance(vResult, Vector)
        self.assertAlmostEqual(vResult.dX, 4.0, 5)
        self.assertAlmostEqual(vResult.dY, 6.0, 5)
        self.assertAlmostEqual(vResult.dZ, 3.0, 5)

        v1 = Vector(1,2, 3)
        v2 = Vector(3,4, 5)
        vResult = v1 + v2
        self.assertIsNotNone(vResult)
        self.assertIsInstance(vResult, Vector)
        self.assertAlmostEqual(vResult.dX, 4.0, 5)
        self.assertAlmostEqual(vResult.dY, 6.0, 5)
        self.assertAlmostEqual(vResult.dZ, 8.0, 5)

    def test_VectorAddition_plusPoint_makesNewPoint(self):
        v1 = Vector(1,2)
        p1 = Point(3,4)
        pResult = p1 + v1
        self.assertIsNotNone(pResult)
        self.assertIsInstance(pResult, Point)
        self.assertAlmostEqual(pResult.X, 4.0, 5)
        self.assertAlmostEqual(pResult.Y, 6.0, 5)
        self.assertIsNone(pResult.Z)

        v1 = Vector(1,2, 101)
        p1 = Point(3,4)
        pResult = p1 + v1
        self.assertIsNotNone(pResult)
        self.assertIsInstance(pResult, Point)
        self.assertAlmostEqual(pResult.X, 4.0, 5)
        self.assertAlmostEqual(pResult.Y, 6.0, 5)
        self.assertIsNone(pResult.Z)

        v1 = Vector(1,20)
        p1 = Point(3,4,50)
        pResult = p1 + v1
        self.assertIsNotNone(pResult)
        self.assertIsInstance(pResult, Point)
        self.assertAlmostEqual(pResult.X, 4.0, 5)
        self.assertAlmostEqual(pResult.Y, 24.0, 5)
        self.assertAlmostEqual(pResult.Z, 50.0, 5)

        v1 = Vector(1,20,222)
        p1 = Point(3,4,50)
        pResult = p1 + v1
        self.assertIsNotNone(pResult)
        self.assertIsInstance(pResult, Point)
        self.assertAlmostEqual(pResult.X, 4.0, 5)
        self.assertAlmostEqual(pResult.Y, 24.0, 5)
        self.assertAlmostEqual(pResult.Z, 272.0, 5)

    def test_PointReflectiveAddition_changesExistingPoint(self):
        v1 = Vector(1,2)
        p1 = Point(3,4)
        p1 += v1
        self.assertIsNotNone(p1)
        self.assertIsInstance(p1, Point)
        self.assertAlmostEqual(p1.X, 4.0, 5)
        self.assertAlmostEqual(p1.Y, 6.0, 5)
        self.assertIsNone(p1.Z)

        v1 = Vector(1,2,103)
        p1 = Point(3,4)
        p1 += v1
        self.assertAlmostEqual(p1.X, 4.0, 5)
        self.assertAlmostEqual(p1.Y, 6.0, 5)
        self.assertIsNone(p1.Z)

        v1 = Vector(1,20)
        p1 = Point(3,4,50)
        p1 += v1
        self.assertAlmostEqual(p1.X, 4.0, 5)
        self.assertAlmostEqual(p1.Y, 24.0, 5)
        self.assertAlmostEqual(p1.Z, 50.0, 5)

        v1 = Vector(1,20,222)
        p1 = Point(3,4,50)
        p1 += v1
        self.assertAlmostEqual(p1.X, 4.0, 5)
        self.assertAlmostEqual(p1.Y, 24.0, 5)
        self.assertAlmostEqual(p1.Z, 272.0, 5)

    def test_VectorChangePropertiesDirectly(self):
        vec = Vector(1, 2)
        vec.dZ = 123.4
        dz = vec.dZ
        self.assertAlmostEqual(dz, 123.4, 5)

    def test_Vector_getMagnitude(self):
        vec = Vector(1,2)
        expected = math.sqrt(5.0)
        actual = vec.magnitude
        self.assertAlmostEqual(expected, actual, 5)

    def test_Vector_setMagnitude(self):
        vec = Vector(1,2)
        vec.magnitude = 1.0
        expectedX = 0.4472135955
        expectedY = 0.894427190999
        actualX = vec.dX
        actualY = vec.dY
        self.assertAlmostEqual(expectedX, actualX, 5)
        self.assertAlmostEqual(expectedY, actualY, 5)

        vec = Vector(1,2,3)
        vec.magnitude = 1.0
        expectedX = 0.267261241913
        expectedY = 0.534522483825
        expectedZ = 0.801783725738
        actualX = vec.dX
        actualY = vec.dY
        actualZ = vec.dZ
        self.assertAlmostEqual(expectedX, actualX, 5)
        self.assertAlmostEqual(expectedY, actualY, 5)
        self.assertAlmostEqual(expectedZ, actualZ, 5)

    def test_VectorVerifyAzimuth(self):
        vec = Vector(1.0, 0)
        expected = 90.0
        actual = vec.azimuth.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        vec = Vector(-1, 1)
        expected = 315.0
        actual = vec.azimuth.asDegreesFloat()
        self.assertAlmostEqual(expected, actual, 5)

        vec = Vector(0,1)
        vec.azimuth = degree.Degree(90)
        self.assertAlmostEqual(1.0, vec.dX, 5)
        self.assertAlmostEqual(0.0, vec.dY, 5)


    def test_VectorSpinVectorByTurnDenominator(self):
        vec = Vector(1,2)
        expected = 26.565051177
        self.assertAlmostEqual(vec.azimuth.asDegreesFloat(), expected, 5)
        vec.spinInXYbyTurns(1 / 4.0)
        expected += 90.0
        self.assertAlmostEqual(vec.azimuth.asDegreesFloat(), expected, 5)

    def test_Vector_addToDeflection(self):
        vec1 = Vector(1,2)
        expected = 26.565051177
        self.assertAlmostEqual(vec1.azimuth.asDegreesFloat(), expected, 5)
        defl = Deflection(degree.Degree(90.0))
        vec2 = vec1 + defl
        expected += 90.0
        self.assertAlmostEqual(vec2.azimuth.asDegreesFloat(), expected, 5)

        defl = Deflection(degree.Degree(-90.0))
        vec3 = vec1 + defl
        expected += 180.0
        self.assertAlmostEqual(vec3.azimuth.asDegreesFloat(), expected, 5)



