from unittest import TestCase
from degree import *
import math

class TestDegree(TestCase):
    def test_asRadiansDouble(self):
        deg = Degree(45.0)
        self.assertTrue(deg.asRadiansDouble() == math.pi / 4.0)

    def test_asDegreesDouble(self):
        deg = Degree(45.0)
        self.assertTrue(deg.asDegreesDouble() == 45.0)

    def test_factoryFromRadians(self):
        deg = Degree.factoryFromRadians(math.pi / 2.0)
        self.assertTrue(deg.asDegreesDouble() == 90.0)

    def test_factory_decimalDegrees(self):
        deg = Degree.factory(12.0)
        self.assertTrue(deg.asDegreesDouble() == 12.0)

    def test_factory_DMS(self):
        deg = Degree.factory(12, 30, 30)
        self.assertTrue(deg.asDegreesDouble() ==
                        12.5 + 30.0 / 3600.0)
