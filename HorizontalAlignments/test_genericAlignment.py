from unittest import TestCase
from genericAlignment import GenericAlignment as GenericAlignment

def alignmentAssert(
        testClass,
        alignment,
        staBeginVal=None,
        staBeginRegion=None,
        staEndVal=None,
        staEndRegion=None,
        alignLength=None
            ):
    testClass.assertIsNotNone(alignment)
    testClass.assertTrue(isinstance(alignment, GenericAlignment))
    if staBeginVal: testClass.assertAlmostEqual(staBeginVal, alignment.BeginStation.station)
    if staBeginRegion: testClass.assertAlmostEqual(staBeginRegion, alignment.BeginStation.region)
    if alignLength: testClass.assertAlmostEqual(alignLength, alignment.Length)
    if staEndVal: testClass.assertAlmostEqual(staEndVal, alignment.EndStation.station)
    if staEndRegion: testClass.assertEqual(staEndRegion, alignment.EndStation.region)

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
        alignmentAssert(self, self.alignment1, staBeginVal=1000.0,
                        staEndVal=2000.0, alignLength=1000.0,
                        staEndRegion=1)

    def test_createGenericAlignment_withRegionListLen1(self):
        alignmentAssert(self, self.alignment2, staBeginVal=1100.0,
                        staEndVal=2250.0, alignLength=1150.0,
                        staBeginRegion=1,staEndRegion=1)

