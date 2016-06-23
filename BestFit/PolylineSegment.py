# unityID = ptschrum
# Paul Schrum
# GIS 540 Course Project

import collections

class PolylineSegment(collections.deque):
    """
    Represents a polyline segment as a list of points plus
    information on which polyline owns the point and the OID
    of the owning segment.  These are superfluous for the course
    project, but I will be using these values soon in other research.
    """
    def __init__(self, iterPoints=None, ParentID=None, parentFCname=None):
        super(PolylineSegment, self).__init__(iterPoints)
        parentOID = ParentID
        parentFC = parentFCname


