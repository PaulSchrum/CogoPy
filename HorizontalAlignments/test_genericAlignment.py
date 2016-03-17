from unittest import TestCase
from genericAlignment import GenericAlignment as GenericAlignment

class TestGenericAlignment(TestCase):
    def setUp(self):
        if not hasattr(self, 'customStuffInitialized'):
            self.customStuffInitialized = True
            self.alignment1 = GenericAlignment(parentAlignment=None,
                                               Name="AL1",
                                               beginStation=1000.0,
                                               length=1000.0,
                                               regionTupleList=None)
            self.alignment2 = GenericAlignment(parentAlignment=None,
                                               Name='AL2',
                                               regionTupleList=[(1100, 2250)])

    def test_createSimpleGenericAlignment(self):
        self.assertIsNotNone(self.alignment1)
        self.assertTrue(isinstance(self.alignment1, GenericAlignment))
        self.assertAlmostEqual(1000.0, self.alignment1.BeginStation.station)
        self.assertAlmostEqual(1000.0, self.alignment1.Length)
        self.assertAlmostEqual(2000.0, self.alignment1.EndStation.station)
        self.assertEqual(1, self.alignment1.EndStation.region)

    def test_createGenericAlignment_withRegionListLen1(self):
        self.assertIsNotNone(self.alignment2)
        self.assertTrue(isinstance(self.alignment2, GenericAlignment))
        self.assertAlmostEqual(1100.0, self.alignment2.BeginStation.station)
        self.assertAlmostEqual(1150.0, self.alignment2.Length)
        self.assertAlmostEqual(2250.0, self.alignment2.EndStation.station)
