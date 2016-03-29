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


