from unittest import TestCase
from HorizontalAlignments.genericAlignment import GenericAlignment as GA
from HorizontalAlignments.station import Station as Station, StationError as StationError

class TestStation(TestCase):
    def setUp(self):
        if not hasattr(self, 'customStuffInitialized'):
            self.customStuffInitialized = True
            self.alignment1 = \
                GA(parentAlignment=None,
                   Name="AL1",
                   beginStation=1000.0,
                   length=1000.0,
                   regionTupleList=None)

    def test_StationArithmatic_NoAlignment(self):
        sta1 = Station(1200.0)
        sta2 = Station(1400.0)
        expected = 200.0
        actual = sta2 - sta1
        self.assertAlmostEqual(expected, actual, 5)
        sta3 = sta1 + 300
        self.assertTrue(isinstance(sta3, Station))
        expected = 1500.0
        actual = sta3.station
        self.assertAlmostEqual(expected, actual, 5)
        self.assertEqual(1, sta3.region)

        sta1 += 150.0
        expected = 1350.0
        actual = sta1.station
        self.assertAlmostEqual(expected, actual, 5)

        sta2 -= 350.0
        expected = 1050.0
        actual = sta2.station
        self.assertAlmostEqual(expected, actual, 5)

    def test_StationArithmatic_Alignment1Region(self):
        sta1 = Station(1200.0,alignment=self.alignment1)
        sta2 = Station(1400.0,alignment=self.alignment1)
        expected = 200.0
        actual = sta2 - sta1
        self.assertAlmostEqual(expected, actual, 5)
        sta3 = sta1 + 300
        self.assertTrue(isinstance(sta3, Station))
        expected = 1500.0
        actual = sta3.station
        self.assertAlmostEqual(expected, actual, 5)
        self.assertTrue(sta3.alignment.name == "AL1")
        self.assertEqual(1, sta3.region)

        # with self.assertRaises(StationError):
        #     sta1 += 123456789.0

        # sta1 += 150.0
        # expected = 1350.0
        # actual = sta1.station
        # self.assertAlmostEqual(expected, actual, 5)

        # sta2 -= 350.0
        # expected = 1050.0
        # actual = sta2.station
        # self.assertAlmostEqual(expected, actual, 5)

    def test_StationArithmatic_Alignment3Regions(self):
        pass