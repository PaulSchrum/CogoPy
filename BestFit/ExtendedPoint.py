"""

"""
import math

class ExtendedPoint():
    """
    Members:
        X - X value (float)
        Y - Y value (float)

                  Note: Some members are not known until method
                      compute_arc_parameters is called.
        Derived Members:
        arc (object) - values related to the arc this point is part of
            arc.degreeCurve  (float) - degree of curve based on deflection
                over 1 unit (meters or feet - on any Planar Coordinate
                System) Derived by equation, set by method, not set by user
            arc.curveCenter (Point or Extended Point) - Circular curve center
                point related to this point (self) as set by method call.
            arc.lengthBack (float) - distance along the arc back to the
                previous point.
            arc.lengthAhead (float) distance along the arc ahead to the
                next point
            arc.deflection - total deflection from back point to ahead point
                as deflected along the arc defined by the three points. Value
                interpreted as radians.
        pt2pt (object) - values related to the points as the vertex of
            a triangle.
            pt2pt.distanceBack (float) - chord distance to previous point
            pt2pt.distanceAhead (float) - chord distance to next point
            pt2pt.deflection (float) -  deflection chord to chord interpreted
                as radians.
    Methods:
        compute_arc_parameters - given 3 points, it computes parameters
            for the arc which passes through the three given points.
            Side Effect: All parameters are attached to the second
            ExtendedPoint parameter.
    """
    def __init__(self, aPoint, newY=None):
        if newY is None:
            self.X = aPoint.X
            self.Y = aPoint.Y
        else:
            self.X = aPoint
            self.Y = newY
        self.degreeCurve = False
        self.curveCenter = False

    def __repr__(self):
        return '{0}, {1}'.format(self.X, self.Y)

    def __add__(self, other):
        return ExtendedPoint(self.X + other.X,
                             self.Y + other.Y)

    def __sub__(self, other):
        return ExtendedPoint(other.X - self.X,
                             other.Y - self.Y)

class IntersectionError(Exception):
    def __init__(self):
        self.message =  "No intersection found for the two items."

class ray2D():
    def __init__(self, extendedPt, azimuth):
        self.extendedPoint = extendedPt
        self.azimuth =  azimuth
        acos = math.cos(azimuth)
        asin = math.sin(azimuth)
        self.slope = math.cos(azimuth) / math.sin(azimuth)
        self.yIntercept = extendedPt.Y - self.slope * extendedPt.X

    def intersectWith(self, otherRay):
        """
        Given this ray and another, find the intersection point of the two.
        :param otherRay: Ray to be intersected
        :return: ExtendedPoint of the Intersection
        :raises: IntersectionError if rays are parallel
        """
        if self.azimuth == otherRay.azimuth:
            raise IntersectionError()
        deltaVec = otherRay.extendedPoint - self.extendedPoint



def getDist2Points(p1, p2):
    """
    returns the distance between two points.
    :param p1: First point (required)
    :param p2: Second point (required)
    :return: float of the distance
    """
    return ((p2.X - p1.X)** 2 + (p2.Y - p1.Y)**2)** 0.5

def getAzimuth(p1, p2):
    """
    Returns the Azimuth of the vector between the two points in which
            0.0 is North, positive is clockwise, and 0.0 <= Azimuth < 360.0
    :param p1: First Point (required)
    :param p2: Second Point (required)
    :return: float of the Azimuth.
    """
    dy = p2.Y - p1.Y
    dx = p2.X - p1.X
    return math.atan2(dx, dy)

def vectorFromDistanceAzimuth(length, az):
    """
    Given a vector in the form of length and azimuth,
        compute the vector values of dX and dY.
    :param length: length of the vector
    :param az: azimuth of the vector
    :return: ExtendedPoint with values X =dX, Y = dY
    """
    dx = length * math.sin(az)
    dy = length * math.cos(az)
    return ExtendedPoint(dx, dy)

def compute_arc_parameters(point1, point2, point3):
    """
    Computes all relevatnt parameters to the trio of points.
    Side Effects: The computed parameters are added to pt2.
    :param point1: Back point
    :param point2: Current point
    :param point3: Ahead point
    :return: None
    """
    point2.pt2pt = object()
    point2.pt2pt.distanceBack = getDist2Points(point2, point1)
    point2.pt2pt.distanceAhead = getDist2Points(point3, point2)
    azimuth12 = getAzimuth(point2, point1)
    azimuth23 = getAzimuth(point3, point2)
    defl = azimuth23 - azimuth12
    if defl < 0.0:
        defl = defl + 2.0 * math.pi
    elif defl > 2.0 * math.pi:
        defl = defl - 2.0 * math.pi

    point2.pt2pt.deflection = defl

    point2.arc = object()
    if defl == 0.0:
        point2.arc.degreeCurve = 0.0
        point2.arc.curveCenter = False
        point2.arc.lengthBack = False
        point2.arc.lengthAhead = False
        point2.arc.deflection = False
        return

    # compute Center point of resulting arc
    # taken from http://stackoverflow.com/a/22792373/1339950
    # Answer to:
    # "Algorithm to find an arc, its center, radius and angles given 3 points"

    # Get center of vec12 a center point of secant1to2
    halfVec12 = vectorFromDistanceAzimuth(point2.pt2pt.distanceBack / 2.0,
                                          azimuth12)
    midPoint12 = point1 + halfVec12

if __name__ == '__main__':
    print 'running module tests for ExtendedPoint.py'
    print

    # Test Point Creation by 2 floats
    point1 = ExtendedPoint(10.0, 20.0)
    assert point1.X == 10.0
    assert point1.Y == 20.0

    point2 = ExtendedPoint(20.0, 25.0)
    distance12 = getDist2Points(point1, point2)
    expected = 11.18033989
    assert math.fabs(distance12 - expected) < 0.0001

    azmuth12 = getAzimuth(point1, point2)
    expected = 1.10714940556
    assert  math.fabs(azmuth12 - expected) < 0.00001

    # Test vector creation
    vec12 = vectorFromDistanceAzimuth(distance12, azmuth12)
    assert math.fabs(vec12.X - 10.0) < 0.00001
    assert math.fabs(vec12.Y - 5.0) < 0.00001

    # Test add Point to Point (treated as a Vector)
    point3 = point1 + point2
    expected = 30.0
    assert math.fabs(point3.X - expected) < 0.00001
    expected = 45.0
    assert math.fabs(point3.Y - expected) < 0.00001

    # Test 2D Ray Creation
    az = math.pi * 0.75
    aRay = ray2D(point1, az)
    expected = -1.0
    assert math.fabs(aRay.slope - expected) < 0.00001
    expected = 30.0
    assert math.fabs(aRay.yIntercept - expected) < 0.000001

    az = math.pi / 2.0
    anotherRay = ray2D(point2, az)

    point4 = aRay.intersectWith(anotherRay)
    expected = 25.0
    assert math.fabs(point4.Y - expected) < 0.0001
    expected = 5.0
    assert math.fabs(point4.Y - expected) < 0.0001

    print 'tests complete.'