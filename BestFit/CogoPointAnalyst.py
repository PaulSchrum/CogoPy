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
from ExtendedPoint import compute_arc_parameters
print 'finished imports'

successList = []


def analyzePolylines(fcs, outDir, loadCSVtoFeatureClass=False,spatialRef=None):
    try:
        validate_or_create_outDir(outDir)
    except:
        print ("Unable to create output directory. No files processed.")

    for fc in fcs:
        try:
            print "Now processing {0}".format(fc)
            csvName = processFCforCogoAnalysis(fc, outDir, spatialRef=spatialRef)
            successList.append(csvName)
            print "File created: {0}".format(csvName)
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


def processFCforCogoAnalysis(fc, outputDir, spatialRef=None):
    """
    Process a Polyline file to analyze its points, generating a csv file of
    the same name, but saved to the output Directory.
    :param fc: Feature Class to be processed.
    :param outputDir: Output directory to put the resulting csv file in.
    :return: the filename of the csv file that was saved (str)
    """
    confirmFCisPolyline(fc)
    alignmentsList = getListOfAlignmentsAsPoints(fc, spatialRef=spatialRef)
    for num, alignment in enumerate(alignmentsList):
        outputFile = _generateOutputFileName(fc, num, outputDir)
        processPointsForCogo(alignment)
        writeToCSV(alignment, outputFile)
    return outputFile

def processPointsForCogo(listOfPoints):
    for pt1, pt2, pt3 in zip(listOfPoints[:-2],
                             listOfPoints[1:-1],
                             listOfPoints[2:]):
        compute_arc_parameters(pt1, pt2, pt3)


def writeToCSV(pointList, fileName):
    """
    :param pointList:
    :return:
    """
    with open(fileName, 'w') as f:
        headerStr = ExtendedPoint.header_list()
        f.write(headerStr + '\n')
        for i, point in enumerate(pointList):
            writeStr = str(point)
            f.write(writeStr + '\n')

def getListOfAlignmentsAsPoints(fc, spatialRef=None):
    """
    Given a feature class (believed to be Polyline), convert each
    contiguous line segment into an spatially ordered list of points.
    :param fc: Feature Class to extract points from
    :return: List of List of Points. Each List of Points represents a single
            alignment.
    :rtype: List of list of ExtendedPoints.
    """
    # Extract all of the segments into a list of segments.
    # Note: A key assumption is that points within a given segment are
    # already spatially ordered
    segmentList = _breakPolylinesIntoSegments(fc, spatialRef=spatialRef)
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


def _breakPolylinesIntoSegments(fc, spatialRef=None, onlyDoSelected=False):
    """
    Given a feature class (Polyline), returns all segments
    broken out as ExtendedPoints.
    :param fc: Feature Class to break into segments.
    :param onlySoSelected: If true, only operate on selected items
    :return: deque of all segments in the feature class
    :rtype: deque (of list of segments)
    """
    #ToDo: implement onlyDoSelected=True
    segmentDeque = collections.deque()
    lines_cursor = arcpy.da.SearchCursor(fc, ["SHAPE@", "OBJECTID"], spatial_reference=spatialRef)
    for lines_row in lines_cursor:
        oid = lines_row[1]
        aPolylineSegment = _PolylineSegment()
        geom = lines_row[0]
        for partIndex in range(geom.partCount):
            geomPart = geom.getPart(partIndex)
            for aPoint in geomPart:
                aPolylineSegment.append(ExtendedPoint(aPoint, parentPK=oid))
        segmentDeque.append(aPolylineSegment)
    return segmentDeque

def _generateOutputFileName(seedName, fileNumber, outDir):
    """
    Takes a feature class name and generates a .csv filename from it
    with the outDir path (instead of the original path).
    :param seedName: Name of feature class to bass output file name on
    :param outDir: Directory to prepend to the seedName
    :rtype: str
    """
    if fileNumber > 0:
        fn = str(fileNumber)
    else:
        fn = ""
    return outDir + '/' + os.path.basename(seedName) + fn + '.csv'


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
    if not (desc.dataType == 'ShapeFile' or desc.dataType == 'FeatureClass'):
        raise NotPolylineError
    if desc.shapeType != 'Polyline':
        raise NotPolylineError

def validate_or_create_outDir(outDir):
    if not os.path.exists(outDir):
        os.makedirs(outDir)

if __name__ == '__main__':
    arcpy.env.workspace = r"C:\GISdata\SelectedRoads.gdb"
    featureClasses = [r'C:\GISdata\SelectedRoads.gdb\LeesvilleRoadRaleigh',
                      r'C:\GISdata\SelectedRoads.gdb\CatesAvenue',
                      r'C:\GISdata\SelectedRoads.gdb\DanAllenDrive',
                      r'C:\GISdata\SelectedRoads.gdb\FaucetteDrive',
                      r'C:\GISdata\SelectedRoads.gdb\MorrillDrive',
                      ]
    neuseRiver = [r"C:\SourceModules\CogoPy\data\other\Neuse401.shp"]
    outputDir = r"C:\GISdata\testOutput"

    analyzePolylines(neuseRiver,
    # analyzePolylines(featureClasses,
                     outputDir,
                     loadCSVtoFeatureClass=False,
                     spatialRef=None)

