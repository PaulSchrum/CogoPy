
from station import Station as Station, StationError as StationError

class GenericAlignment(object):
    def __init__(self,
                 parentAlignment,
                 Name=None,
                 beginStation=None,
                 length=None,
                 regionTupleList = None
                 ):
        '''
        If parentAlignment is not None, only length should be set.
        Otherwise . . .
        If regionTupleList is None, beginStation and length must be not None.
        If regionTupleList is not None, beginStation and length are ignored.
        :param parentAlignment: GenericAlignment
        :param Name: String
        :param beginStation: (float, int, long)
        :param length: (float, int, long)
        :param regionTupleList:
        :return:
        '''

        self.parentAlignment = parentAlignment
        self.name = Name
        # self._beginStation=beginStation
        # self._length = length
        if parentAlignment is None:
            if regionTupleList is not None:
                self._regionList = _regionList(regionTupleList)
            elif beginStation is not None and length is not None:
                self._regionList = _regionList([(beginStation,
                                                beginStation + length)])
            else:
                raise ValueError("If regionTupleList is None, then beginStation and length must be not None.")
        else:
            self._regionList = None


    @property
    def EndStation(self):
        return Station(self._regionList[-1].endStation, len(self._regionList), self)

    @property
    def BeginStation(self):
        if self.parentAlignment is None:
            retStation = Station(self._regionList[0].beginStation, 1, self)
            return retStation
        else:
            pass

    @BeginStation.setter
    def BeginStation(self, newVal):
        if self.parentAlignment is None:
            if isinstance(newVal, (int, long, float)):
                self._beginStation = newVal
            elif isinstance(newVal, Station):
                self._beginStation = newVal
            else:
                raise TypeError("BeginStation may only be float, int, long, or Station.")
        else:
            self.validateStation()

    @property
    def Length(self):
        if self.parentAlignment is None:
            return self._regionList[-1].trueEndStation

    @Length.setter
    def Length(self, newVal):
        if not isinstance(newVal, (float, int, long)):
            raise TypeError("Length must be a Real number of any kind.")
        self._length = newVal

    def getTrueStation(self, stationNumber, region):
        try:
            regio = self._regionList[region-1]
        except IndexError:
            raise StationError("Region is not on this alignment.")
        distanceInto = stationNumber - regio.beginStation
        if distanceInto < 0.0:
            raise StationError(
                "Station is not on region {0} of this alignment.".
                format(region))
        if distanceInto > regio.length + self._TOLERANCE:
            raise StationError(
                "Station is not on region {0} of this alignment.".
                format(region))
        return distanceInto + regio.trueBeginStation

    @property
    def _TOLERANCE(self):
        return 0.0000001

    def getStationRegion(self, trueStation):
        if trueStation < 0:
            raise StationError("Absolute Station may not be less than 0.0.")
        # trueBeginStation
        regionCount = 0
        testIsTrue =  self._regionList[regionCount].absStaIsInMyRange(trueStation)
        if trueStation > self.EndStation.trueStation:
            raise StationError("Given Absolute Station is off end of alignment.")
        while not testIsTrue:
            regionCount += 1
            testIsTrue =  self._regionList[regionCount].absStaIsInMyRange(trueStation)

        sta = trueStation - self._regionList[regionCount].trueBeginStation
        sta += self._regionList[regionCount].beginStation
        return sta, regionCount+1

        # except IndexError:
        #     raise StationError("True Station is beyond end of alignment.")
        return trueStation - self._regionList[regionCount].trueBeginStation, regionCount

    def validateStation(self, aStation):
        if not isinstance(aStation, Station):
            raise StationError("Variable is not of class 'Station'.")
        if not self is aStation.alignment:
            raise StationError("Given variable is not associated with this alignment.")
        reg = aStation.region
        if reg > len(self._regionList) or reg < 1:
            raise StationError("Region is not on this alignment.")
        begSta = self._regionList[reg-1].beginStation
        if aStation.station < begSta:
            raise StationError("Station is not on region {0} of this alignment.".
                               format(reg))
        endSta = self._regionList[reg-1].endStation
        if aStation.station > endSta:
            raise StationError("Station is not on region {0} of this  alignment.".
                               format(reg))

    def appendRegion(self, stationValueTuple):
        if not isinstance(stationValueTuple, tuple):
            raise TypeError("Parameter must be of type Tuple.")
        if len(stationValueTuple) != 2:
            raise ValueError("Station Value Tuple must have 2 and only 2 members.")
        bSta = stationValueTuple[0]
        eSta = stationValueTuple[1]
        if self._regionList is None:
            self._regionList = []
        self._regionList.append(stationValueTuple)
        if len(self._regionList) == 1:
            self._beginStation = bSta
            self._length = eSta - bSta

    def getStationFromTrueStation(self, trueStation):
        if trueStation < 0:
            raise StationError("True station may not be less than 0.0.")
        regNo = 0
        for reg in self._regionList:
            regNo += 1
            if reg.absStaIsInMyRange(trueStation):
                staVal = trueStation - reg.trueBeginStation + reg.beginStation
                return Station(station=staVal, region=regNo, alignment=self)
        raise StationError("True station is greater than alignment's trueEndStation")


class _region():
    def __init__(self,
                 beginStation,
                 endStation=None):
        """
        Creates a new instance of a region.
        :param beginStation: float
        :param endStation: float. May be None if end station is not known.
        :return: N/A
        """
        self.beginStation = beginStation
        self.endStation = endStation
        self.trueBeginStation = 0.0
        self.trueEndStation = 0.0

    @property
    def length(self):
        return self.trueEndStation - self.trueBeginStation

    def absStaIsInMyRange(self, aTrueStation):
        if aTrueStation < self.trueBeginStation:
            return False
        elif aTrueStation > self.trueEndStation:
            return False
        return True

class _regionList(list):
    def __init__(self, rListTuples):
        list.__init__(self)
        cummLen = 0.0
        for r in rListTuples:
            newReg = _region(beginStation=r[0],
                              endStation=r[1])
            newReg.trueBeginStation = cummLen
            cummLen += newReg.endStation - newReg.beginStation
            newReg.trueEndStation = cummLen
            self.append(newReg)

