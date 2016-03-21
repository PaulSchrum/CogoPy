
import genericAlignment

class Station():
    def __init__(self, station, region=None, alignment=None):
        """
        Station is a location along an alignment.
        :param station: Station Value (float or int)
        :param region: Region Number (int only)
        :param alignment: Parent Alignment, may be None (GenericAlignment
        :return: None
        """
        self.station = station
        if region is not None:
            self.region = region
        else:
            self.region = 1

        if alignment is not None and not isinstance(alignment, genericAlignment.GenericAlignment):
            raise TypeError("alignment parameter must be subclass of GenericAlignment")
        self.alignment = alignment
        if alignment is not None:
            self.trueStation = self.alignment.getTrueStation(station, self.region)
        else:
            self.trueStation = station

    @property
    def trueStation(self):
        if self.alignment is None:
            return self.station
        else:
            return self.alignment.getTrueStation(self.station, self.region)

    def __add__(self, other):
        if self.alignment is None:
            return Station(self.station + other)
        else:
            sta, reg = self.alignment.getStationRegion(self.trueStation + other)
            return Station(station=sta, region=reg, alignment=self.alignment)

    # Todo: Add __radd__(float) to alter current station
    def __radd__(self, other):
        raise NotImplementedError
        # if self.alignment is None:
        #     return Station(self.station + other)
        # else:
        #     sta, reg = self.alignment.getStationRegion(self.trueStation + other)
        #     return Station(station=sta, region=reg, alignment=self.alignment)

    def __sub__(self, other):
        if isinstance(other, Station) and self.alignment == other.alignment:
            if self.alignment is None:
                return self.station - other.station
            else:
                return self.trueStation - other.trueStation
        elif isinstance(other, (float, int, long)):
            if self.alignment is None:
                return Station(self.station - float(other))

    # Todo: Add __rsub__ (Station) to alter current station
    def __rsub__(self, other):
        raise NotImplementedError


class StationError(Exception):
    def __init__(self, station=None, msg=None):
        if msg is None:
            self.message = "Station Error."
        else:
            self.message = msg

        if station is not None:
            self.station = station

