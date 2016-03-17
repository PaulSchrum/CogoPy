
import genericAlignment

class Station():
    def __init__(self, station, region, alignment):
        """
        Station is a location along an alignment.
        :param station: Station Value (float or int)
        :param region: Region Number (int only)
        :param alignment: Parent Alignment, may be None (GenericAlignment
        :return: None
        """
        self.station = station
        self.region = region

        if alignment is not None and not isinstance(alignment, genericAlignment.GenericAlignment):
            raise TypeError("alignment parameter must be subclass of GenericAlignment")
        self.alignment = alignment

    # Todo: Add trueStation property (after GenericAlignment can handle that)
    @property
    def trueStation(self):
        if self.alignment is None:
            return self.station
        else:
            return self.alignment.getTrueStation(self.station, self.region)

    # Todo: Add __add__ and __radd__(float) to return new station
    # Todo: Add __sub__ and __rsub__ (Station) to return float of the length along

class StationError(Exception):
    def __init__(self, station=None, msg=None):
        if msg is None:
            self.message = "Station Error."
        else:
            self.message = msg

        if station is not None:
            self.station = station

