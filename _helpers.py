
from math import fabs

equalityTolerance = 0.00005

def nearlyEqual(float1, float2, tolerance=equalityTolerance):
    return fabs(float2 - float1) <= tolerance

