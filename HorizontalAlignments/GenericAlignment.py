

class GenericAlignment(object):
    def __init__(self,
                 parentAlignment,
                 beginStation=None,
                 length=None, myIndex=None):
        self.parentAlignment = parentAlignment
        self._beginStation=beginStation
        self._length = length
        self._myIndex = myIndex

    @property
    def EndStation(self):
        return 1.0

    @property
    def BeginStation(self):
        if self.parentAlignment is None:
            if self._beginStation is None:
                return 0.0
            else:
                return self._beginStation
        else:
            pass



class __region():
    def __init__(self, parentAlignment,
                 beginStation,
                 endStation=None,
                 trueBeginStation=None):
        """
        Creates a new instance of a region.
        :param parentAlignment: GenericAlignment
        :param beginStation: float
        :param endStation: float. May be None if end station is not known.
        :return: N/A
        """
        assert isinstance(parentAlignment, GenericAlignment)
        self.parentAlignment = parentAlignment
        self.beginStation = beginStation
        self.endStation = endStation
        self.trueBeginStation = trueBeginStation

    @property
    def length(self):
        if self.endStation is None:
            return self.parentAlignment.__getEndStation() - self.beginStation
        else:
            return self.endStation - self.beginStation

    @property
    def trueEndStation(self):
        return self.trueBeginStation + self.length



