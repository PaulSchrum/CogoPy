# unityID = ptschrum
import collections

class PolylineSegment(collections.deque):
    def __init__(self, iterPoints=None, ParentID=None, parentFCname=None):
        super(PolylineSegment, self).__init__(iterPoints)
        parentOID = ParentID
        parentFC = parentFCname


