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
            arc.curveCenterPoint (Point or Extended Point) - Circular curve center
                point related to this point (self) as set by method call.
            arc.lengthBack (float) - distance along the arc back to the
                previous point.
            arc.lengthAhead (float) distance along the arc ahead to the
                next point
            arc.deflection - total deflection from back point to ahead point
                as deflected along the arc defined by the three points. Value
                interpreted as radians.
            arc.radiusStartVector - vector from curve center to Point1 (begin point)
            arc.radiusEndVector - vector from curve center to Point3 (end point)
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
        self.pt2pt = False
        self.arc = False

    def __repr__(self):
        return '{0}, {1}: Mag {2}  Az {3}'.format(self.X,
                                                  self.Y,
                                                  self.magnitude,
                                                  self.azimuth)

    def __add__(self, other):
        return ExtendedPoint(self.X + other.X,
                             self.Y + other.Y)

    def __sub__(self, other):
        return ExtendedPoint(other.X - self.X,
                             other.Y - self.Y)

    @property
    def magnitude(self):
        return math.sqrt(self.X * self.X + self.Y * self.Y)

    @property
    def azimuth(self):
        return math.atan2(self.X, self.Y)

class struct():
    '''
    Named for and serving a similar purpose as the C concept of Struct.
    This class exists as something to add attributes to dynamically.
    '''
    pass

class IntersectionError(Exception):
    def __init__(self):
        self.message =  "No intersection found for the two items."

class Ray2D():
    '''
    Represents a bidirectional ray, usually used for finding intersections.
    Also known as a line (as in, unbounded line).
    If the ray is vertical, slope and yIntercept are float("inf")
    '''
    def __init__(self, extendedPt, azimuth):
        self.extendedPoint = extendedPt
        self.azimuth =  azimuth
        acos = math.cos(azimuth)
        asin = math.sin(azimuth)
        if azimuth == 0.0:
            self._slope = float("inf")
        elif azimuth == math.pi:
            self._slope = float("inf")
        else:
            self._slope = math.cos(azimuth) / math.sin(azimuth)
        self._yIntercept = extendedPt.Y - self.slope * extendedPt.X

    @property
    def slope(self):
        return self._slope

    @property
    def yIntercept(self):
        return self._yIntercept

    def __repr__(self):
        if self.slope == float(inf):
            str = 'Vertical @ X = {0}'.format(self.extendedPoint.X)
        else:
            str = 'Slope: {0}  yIntercept: {1}'.format(self.slope,
                                                       self.yIntercept)
        return str

    def given_X_get_Y(self, xValue):
        '''Return Y using the y = mx + b equation of a line.'''
        return self.slope * xValue + self.yIntercept

    def given_Y_get_X(self, yValue):
        '''Return X using y = mx + b solved for x.'''
        if self.slope == float("inf"):
            return self.extendedPoint.X
        return (yValue - self.yIntercept) / self.slope

    def intersectWith(self, otherRay):
        """
        Given this ray and another, find the intersection point of the two.
        :param otherRay: Ray to be intersected
        :return: ExtendedPoint of the Intersection
        :raises: IntersectionError if rays are parallel
        """
        if self.azimuth == otherRay.azimuth:
            raise IntersectionError()
        if math.isinf(otherRay.slope):
            newX = otherRay.extendedPoint.X
            newY = self.yIntercept + self.slope * newX
        elif math.isinf(self.slope):
            newX = self.extendedPoint.X
            newY = otherRay.yIntercept + otherRay.slope * newX
        else:
            yInt = self.yIntercept
            newX = (otherRay.yIntercept - yInt) / \
                 (self.slope - otherRay.slope)
            newY = self.yIntercept + self.slope * newX
        return ExtendedPoint(newX, newY)

    @staticmethod
    def get_bisecting_normal_ray(firstPt, otherPt):
        '''
        Given this point and another, return the ray which bisects the
            line segment between the two.
        :rtype: Ray2D
        :param otherPt: Second point of the line segment to be bisected.
        :return: Ray2d with origin point at the bisector of the line segment
            and ahead direction 90 degrees to the right of the line segment.
        '''
        if otherPt.pt2pt:
            distBack = otherPt.pt2pt.distanceBack
        else:
            distBack = getDist2Points(firstPt, otherPt)
        az12 = getAzimuth(firstPt, otherPt)
        halfVec12 = vectorFromDistanceAzimuth(distBack / 2.0, az12)
        midPoint12 = firstPt + halfVec12
        return Ray2D(midPoint12, az12 + math.pi / 2.0)

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
    :rtype: ExtendedPoint
    :param length: length of the vector
    :param az: azimuth of the vector
    :return: ExtendedPoint with values X =dX, Y = dY, being considered a vector
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
    point2.pt2pt = struct()
    point2.pt2pt.distanceBack = getDist2Points(point2, point1)
    point2.pt2pt.distanceAhead = getDist2Points(point3, point2)
    azimuth12 = getAzimuth(point1, point2)
    azimuth23 = getAzimuth(point2, point3)
    defl = azimuth23 - azimuth12
    if defl < 0.0:
        defl = defl + 2.0 * math.pi
    elif defl > 2.0 * math.pi:
        defl = defl - 2.0 * math.pi

    point2.pt2pt.deflection = defl

    point2.arc = struct()
    if defl == 0.0:
        point2.arc.degreeCurve = 0.0
        point2.arc.radius = float('inf')
        point2.arc.curveCenter = False
        point2.arc.lengthBack = False
        point2.arc.lengthAhead = False
        point2.arc.radiusStartVector = False
        point2.arc.radiusEndVector = False
        point2.arc.deflection = 0.0
        return

    # compute Center point of resulting arc
    # taken from http://stackoverflow.com/a/22792373/1339950
    # Answer to:
    # "Algorithm to find an arc, its center, radius and angles given 3 points"

    # Get the ray bisecting and normal to secant12 and secant23
    biRay12 = Ray2D.get_bisecting_normal_ray(point1, point2)
    biRay23 = Ray2D.get_bisecting_normal_ray(point2, point3)

    point2.arc.curveCenter = biRay12.intersectWith(biRay23)

    point2.arc.radiusStartVector = point2.arc.curveCenter - point1
    point2.arc.radiusEndVector = point2.arc.curveCenter - point3
    point2.arc.degreeCurve = 1.0 / point2.arc.radiusEndVector.magnitude
    point2.arc.deflection = point2.arc.radiusEndVector.azimuth - point2.arc.radiusStartVector.azimuth

    p2Vector = point2.arc.curveCenter - point2
    defl12 = p2Vector.azimuth - point2.arc.radiusStartVector.azimuth
    defl23 = point2.arc.deflection - defl12
    point2.arc.lengthBack = defl12 * point2.arc.radiusStartVector.magnitude
    point2.arc.lengthAhead = defl23 * point2.arc.radiusStartVector.magnitude

def _assertFloatsEqual(f1, f2):
    '''Test whether two floats are approximately equal.
    The idea for the added message comes from
    http://stackoverflow.com/a/3808078/1339950
    '''
    customMessage = "{0} does not equal {1}".format(f1, f2)
    assert math.fabs(f1 - f2) < 0.000001, customMessage

def _assertPointsEqualXY(p1, p2):
    '''Test whether two points are approximately equal.
    Only tests equality of X and Y.  Other extended properties
    are ignored
    '''
    customMessage = "{0} does not equal {1}".format(p1, p2)
    assert math.fabs(p1.X - p2.X) < 0.000001, customMessage
    assert math.fabs(p1.Y - p2.Y) < 0.000001, customMessage

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
    _assertFloatsEqual(distance12, expected)

    azmuth12 = getAzimuth(point1, point2)
    expected = 1.10714940556
    _assertFloatsEqual(azmuth12, expected)

    # Test vector creation
    vec12 = vectorFromDistanceAzimuth(distance12, azmuth12)
    expected = ExtendedPoint(10.0, 5.0)
    _assertPointsEqualXY(vec12, expected)

    # Test add Point to Point (treated as a Vector)
    point3 = point1 + point2
    expected = ExtendedPoint(30.0, 45.0)
    _assertPointsEqualXY(point3, expected)

    # Test 2D Ray Creation
    az = math.pi * 0.75
    aRay = Ray2D(point1, az)
    expected = -1.0
    _assertFloatsEqual(aRay.slope, expected)
    expected = 30.0
    _assertFloatsEqual(aRay.yIntercept, expected)

    az = math.pi / 4.0
    anotherRay = Ray2D(point2, az)
    expected = 1.0
    actual = anotherRay.given_Y_get_X(6.0)
    _assertFloatsEqual(actual, expected)
    expected = 6.0
    actual = anotherRay.given_X_get_Y(1.0)
    _assertFloatsEqual(actual, expected)

    # Test ray intersecting another ray
    point4 = aRay.intersectWith(anotherRay)
    expected = ExtendedPoint(12.5, 17.5)
    _assertPointsEqualXY(point4, expected)

    # Test ray intersecting a vertical ray
    verticalRay = Ray2D(ExtendedPoint(11.0, 1.0), math.pi)
    point5 = aRay.intersectWith(verticalRay)
    expected = ExtendedPoint(11.0, 19.0)
    _assertPointsEqualXY(point5, expected)

    point5 = verticalRay.intersectWith(aRay)
    expected = ExtendedPoint(11.0, 19.0)
    _assertPointsEqualXY(point5, expected)

    # Test get_bisecting_normal_ray
    p1 = ExtendedPoint(0, 0)
    p2 = ExtendedPoint(10, 10)
    aRay = Ray2D.get_bisecting_normal_ray(p1, p2)
    expected = ExtendedPoint(5.0, 5.0)
    _assertPointsEqualXY(aRay.extendedPoint, expected)
    expected = -1.0
    _assertFloatsEqual(aRay.slope, expected)
    expected = 10
    _assertFloatsEqual(aRay.yIntercept, expected)

    # test creation of arc values from 3 points
    # the attributes are added to pt2.
    pt2Coord = (9.0 / math.sqrt(2.0)) + 1.0
    p1 = ExtendedPoint(1,10)
    p2 = ExtendedPoint(pt2Coord, pt2Coord)
    p3 = ExtendedPoint(10,1)
    compute_arc_parameters(p1, p2, p3)
    expected = ExtendedPoint(1,1)
    _assertPointsEqualXY(p2.arc.curveCenter, expected)
    expected = 1.0 / 9.0
    _assertFloatsEqual(p2.arc.degreeCurve, expected)
    expected = math.pi / 2.0
    _assertFloatsEqual(p2.arc.deflection, expected)
    expected = 9.0 * math.pi / 4.0
    _assertFloatsEqual(p2.arc.lengthAhead, expected)
    _assertFloatsEqual(p2.arc.lengthBack, expected)

    print 'tests complete.'