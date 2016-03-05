'''
BoundingBox class
By Paul Schrum. 3/5/2016
'''
import point

class BoundingBox:
    def __init__(self, LLpoint=None, URpoint=None):
        if LLpoint is None:
            self.LowerLeft = point.Point()
            self.UpperRight = point.Point()
        if URpoint is None:
            self.LowerLeft = LLpoint
            self.UpperRight = LLpoint
        else:
            self.LowerLeft = LLpoint
            self.UpperRight = URpoint

    @property
    def LowerLeft(self):
        return self.__LL
    @LowerLeft.setter
    def LowerLeft(self, val):
        assert isinstance(val, point.Point)
        self.__LL = val

    @property
    def UpperRight(self):
        return self.__UR
    @UpperRight.setter
    def UpperRight(self, val):
        assert isinstance(val, point.Point)
        self.__UR = val


