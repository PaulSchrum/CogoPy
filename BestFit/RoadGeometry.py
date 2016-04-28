# Paul Schrum   Unity ID: ptschrum
# GIS 540 Course Project
"""
This file is the Entry Point for the course project.
Call this file from the associated ArcMap custom tool:
Road Geometry Analysis.

Usage:
(code-only)
sys.argv[1] contains list of Polyline files to analyze.
sys.argv[2] contains the directory where output csv files will be stored.
sys.argv[3] ('true' or 'false') If true, load the csv file back in
     as a Polyline feature class to verify that the points are correct.

Usage from within ArcMap:
Open the tool from my toolbox. (Road Geometry Analysis)
> In Feature Classes to Analyze
    Put one or more Polyline feature classes
        (Such as NeuseRiver.shp or LeesvilleRoadRaleigh)

>  In Output CSV Path
    Put a directory.  File names are auto-generated based on
        feature class names.  You will find the resulting CSV
        files in this directory after a successful run. Note,
        the CSV file and the Radius Information associated with
        each point in the CSV file are the primary analysis
        product of the tool.

> Select Create New Shapefile From Analysis Results
    only if you want the tool to back-load another shape file
    from the resulting CSV file(s) as a confidence check.  If
    turned on, the tool automatically appends "_check" to the
    name of the new shapefile, loads it to the default gdb file,
    and adds it to the active Layer for display in the map.

> Select the OK button and the tool runs.

That's all there is to it.

Open the resulting CSV file with Excel to see the results.
Correlating a point (via coordinates) in the CSV file to
the same point on the screen is a little cumbersome.  Sorreez.
"""

import sys
import arcpy
from CogoPointAnalyst import analyzePolylines

inputs = sys.argv[1].split(';')
outDir = sys.argv[2]

createNewShapefile = False
if sys.argv[3] == 'true':
    createNewShapefile = True

mxd = arcpy.mapping.MapDocument('CURRENT')
dfSr = mxd.activeDataFrame.spatialReference
arcpy.AddMessage(' ')
arcpy.AddMessage("All feature classes will be processed in the current data frame's coordinate system:")
arcpy.AddMessage(dfSr.name)
arcpy.AddMessage(' ')

analyzePolylines(inputs,outDir,createNewShapefile,dfSr)
