from unittest import TestCase
from HorizontalAlignments.genericAlignment import GenericAlignment as GenericAlignment

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
            self.alignment3 = GenericAlignment(
                               parentAlignment=None,
                               Name='3Regions',
                               regionTupleList=[
                                   (1000,3300)
                                   ,(10000.5, 10050.6)
                                   ,(500.7,1100.1)
                                    ])

    def test_createSimpleGenericAlignment(self):
        alignmentAssert(self, self.alignment1, staBeginVal=1000.0,
                        staEndVal=2000.0, alignLength=1000.0,
                        staEndRegion=1)

    def test_createGenericAlignment_withRegionListLen1(self):
        alignmentAssert(self, self.alignment2, staBeginVal=1100.0,
                        staEndVal=2250.0, alignLength=1150.0,
                        staBeginRegion=1,staEndRegion=1)

    def test_GenericAlignment_with3Regions(self):
        alignmentAssert(self, self.alignment3, staBeginVal=1000.0,
                        staEndVal=1100.1, alignLength=2949.5,
                        staBeginRegion=1,staEndRegion=3)

