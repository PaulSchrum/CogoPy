"""
CogoPointAnalyst
Tightly bound to arcpy?
"""

__author__ = ['Paul Schrum']

print 'starting imports'
import sys
import os
from arcpy.arcobjects.arcobjects import Point as arcPoint
import arcpy
import collections
from ExtendedPoint import ExtendedPoint
from ExtendedPoint import any_in_point_equals_any_in_other

print 'finished imports'

successList = []


def analyzePolylines(fcs, outDir, loadCSVtoFeatureClass=False):
    for fc in fcs:
        try:
            csvName = processFCforCogoAnalysis(fc, outDir)
            successList.append(csvName)
        except NotPolylineError:
            print "{0} not processed because it " + \
                  "is not a Polyline Feature Class.".format(fc)
        except arcpy.ExecuteError:
            print "Arc Error while processing Feature Class: {0}".format(fc)
        except Exception as e:
            print "Unexpected error: {0}".format(e.message)
            raise

    # if loadCSVtoFeatureClass:
    if 1 == 0:
        tempPoints = 'tempPoints___'
        try:
            for csv in successList:
                arcpy.MakeXYEventLayer_management(csv, 'X', 'Y', tempPoints)
                newLayerName = os.path.basename(csv)
                arcpy.PointsToLine_management(tempPoints, )
        finally:
            arcpy.Delete_management(tempPoints)


def processFCforCogoAnalysis(fc, outputDir):
    """
    Process a Polyline file to analyze its points, generating a csv file of
    the same name, but saved to the output Directory.
    :param fc: Feature Class to be processed.
    :param outputDir: Output directory to put the resulting csv file in.
    :return: the filename of the csv file that was saved (str)
    """
    confirmFCisPolyline(fc)
    outputFile = _generateOutputFileName(fc, outputDir)
    alignmentsList = getListOfAlignmentsAsPoints(fc)
    # for alignment in alignmentsList:
    #     processPointsForCogo(alignment)
    #     writeToCSVfile(alignment, outputFile)
    return outputFile


def _writeToCSV(segmentList, fileName):
    """
    Temp method.  Intended to be deleted before submittal.
    write segmentList to csv file to assist in problem diagnosis.
    :param segmentList:
    :return:
    """
    countr, id = -1, -1
    with open(fileName, 'w') as f:
        f.write('OID,segId,X,Y\n')
        for segment in segmentList:
            countr = countr + 1
            for pt in segment:
                id = id + 1
                writeStr = '{0},{1},{2},{3}\n'.format(id, countr, pt.X, pt.Y)
                f.write(writeStr)
    sys.exit()


def getListOfAlignmentsAsPoints(fc):
    """
    Given a feature class (believed to be Polyline), convert each
    contiguous line segment into an spatially ordered list of points.
    :param fc: Feature Class to extract points from
    :return: List of List of Points. Each List of Points represents a single
            alignment.
    """
    # Extract all of the segments into a list of segments.
    # Note: My understanding is that points within a given segment are
    # already spatially ordered
    segmentList = _breakPolylinesIntoSegments(fc)
    # _writeToCSV(segmentList, 'segmentListDump.csv')

    alignmentList = []
    while len(segmentList) > 0:
        pointList = getPointListFromSegmentList(segmentList)
        alignmentList.append(pointList)

    return alignmentList


def getPointListFromSegmentList(segmentDeque):
    """
    Gets a point list (spatially ordered) from a Deque of Polyline Segments.
    (The Polyline Segments have already been reduced to just points.)
    As a Polyline Segment is added to the return list, it is removed from the
    segmentDeque.  If more than one alignment have been passed to this function,
    it will only remove the segments which are colinear with the first segment.
    Thus len(segmentDeque) will not == 0.
    :param segmentList: Deque containing all of the Polyline Segments
    :return: List of Points that are spatially ordered from beginning to end.
    """
    # Check for adjacency going to the right
    currentSegment = segmentDeque.popleft()
    orderedSegments = collections.deque()
    orderedSegments.append(currentSegment)
    firstSegment = currentSegment
    matchingSegment = True
    while matchingSegment:
        matchingSegment = False
        for i in xrange(len(segmentDeque)):
            matches = any_in_point_equals_any_in_other(currentSegment.endPoints,
                                                       segmentDeque[0].endPoints)
            if matches:
                testSegment = segmentDeque.popleft()
                if matches[0] == 0:  # if current's begin point is the match
                    currentSegment.reverse()
                if matches[1] == 1:  # if test's end point is the match
                    testSegment.reverse()
                testSegment.popleft() # eliminates duplicate point
                orderedSegments.append(testSegment)
                currentSegment = testSegment
                matchingSegment = True
                break
            segmentDeque.rotate(-1)  # for performance since deque is a linked list

    # Check for adjaceny going to the left

    # flatten all points to a single list
    # orderPoints = [pt for seg in orderedSegments for pt in seg]
    orderedPoints = []
    for seg in orderedSegments:
        for pt in seg:
            orderedPoints.append(pt)

    return orderedPoints


class _PolylineSegment(collections.deque):
    @property
    def endPoints(self):
        return self[0], self[-1]


def _breakPolylinesIntoSegments(fc):
    """
    Given a feature class (Polyline), returns all segments
    broken out as ExtendedPoints.
    :param fc: Feature Class to break into segments.
    :return: deque of all segments in the feature class
    :rtype: deque (of list of points)
    """
    segmentList = collections.deque()
    segID = -1
    lines_cursor = arcpy.da.UpdateCursor(fc, ["SHAPE@", "OBJECTID"])
    for lines_row in lines_cursor:
        aPolylineSegment = _PolylineSegment()
        segID = segID + 1
        aPolylineSegment.segID = segID
        geom = lines_row[0]
        for partIndex in range(geom.partCount):
            geomPart = geom.getPart(partIndex)
            for aPoint in geomPart:
                aPolylineSegment.append(ExtendedPoint(aPoint))
        segmentList.append(aPolylineSegment)
    return segmentList


def _generateOutputFileName(seedName, outDir):
    """
    Takes a feature class name and generates a .csv filename from it
    with the outDir path (instead of the original path).
    :param seedName: Name of feature class to bass output file name on
    :param outDir: Directory to prepend to the seedName
    :rtype: str
    """
    return outDir + '/' + os.path.basename(seedName) + '.csv'


class NotPolylineError(TypeError):
    pass


def confirmFCisPolyline(fc):
    """
    If the parameter fc is an ArcGIS polyline, the function does nothing.
    If it is not a polyline, it raises NotPolylineError
    :param fc:
    :return: None
    :raises: NotPolylineError
    """
    desc = arcpy.Describe(fc)
    if not (desc.dataType == 'Shapefile' or desc.dataType == 'FeatureClass'):
        raise NotPolylineError
    if desc.shapeType != 'Polyline':
        raise NotPolylineError


if __name__ == '__main__':
    arcpy.env.workspace = r"C:\GISdata\SelectedRoads.gdb"
    featureClasses = [r'C:\GISdata\SelectedRoads.gdb\LeesvilleRoadRaleigh']
    outputDir = r"C:\GISdata\testOutput"

    analyzePolylines(featureClasses, outputDir, False)

else:
    featureClasses = sys.argv[1]
    outputDir = sys.argv[2]
    loadCSVsAsACheck = None
    if len(sys.argv) > 3:
        loadCSVsAsACheck = sys.argv[3]
    analyzePolylines(featureClasses, outputDir, False)
