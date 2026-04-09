<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Points > Accessing Points in a File -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F64DD398-AE33-47A2-90D2-653DBFA23664.htm -->

# Accessing Points in a File

The AeccPoints object also has methods for reading and writing point locations in a file. The AeccPoints.ImportPoints method creates points from locations stored in a text file. The AeccPoints.ExportPoints method writes point locations to a text file.

The second parameter of the ImportPoints and ExportPoints methods is a string that describes how the point values are stored in the file. The following table lists some commonly available file formats. You can create other formats by using the Point File Format dialog box.

Point File FormatsString Literal | Format of values in the file  
---|---  
ENZ (comma delimited) | Easting, Northing, Elevation  
NEZ (space delimited) | Northing Easting Elevation  
NEZ (comma delimited) | Northing, Easting, Elevation  
PENZ (space delimited) | Point# Easting Northing Elevation  
PENZ (comma delimited) | Point#, Easting, Northing, Elevation  
PENZD (space delimited) | Point# Easting Northing Elevation Description  
PENZD (comma delimited) | Point#, Easting, Northing, Elevation, Description  
PNE (space delimited) | Point# Northing Easting  
PNE (comma delimited) | Point#, Northing, Easting  
PNEZ (space delimited) | Point# Northing Easting Elevation  
PNEZ (comma delimited) | Point#, Northing, Easting, Elevation  
PNEZD (space delimited) | Point# Northing Easting Elevation Description  
PNEZD (comma delimited) | Point#, Northing, Easting, Elevation, Description  
ENZ (space delimited) | Easting Northing Elevation  
Autodesk Uploadable File | Point# Northing Easting Elevation Description  
  
The third parameter of the ImportPoints method is an object of type AeccPointImportOptions, which can be set to perform actions as the data is being loaded. For example, you can add offsets to the point positions or elevations, determine which points to read from the file, or specify the point group where the points are placed. The third parameter of the ExportPoints method is of the similar AeccPointExportOptions type.

This example demonstrates the ImportPoints and ExportPoints methods:
    
    
    Dim oPoints As AeccPoints
    Dim oImportOptions As New AeccPointImportOptions
    Dim sFilename As String
    Dim sFileFormat As String
    Dim iCount As Integer
     
    Set oPoints = oDocument.Points
    sFilename = "C:\My Documents\SamplePointFile.txt"
    sFileFormat = "PENZ (space delimited)"
    oImportOptions.PointDuplicateResolution = aeccPointDuplicateOverwrite
    iCount = oPoints.ImportPoints(sFilename, sFileFormat, oImportOptions)
     
    ' Export the files to a separate file.
    Dim oExportOptions As New AeccPointExportOptions
    sFilename = "C:\My Documents\SamplePointFile2.txt"
    oExportOptions.ExpandCoordinateData = True
    oPoints.ExportPoints sFilename, sFileFormat, oExportOptions
    

Note:

When you add points using the ImportPoints method, it is possible that the point numbers will conflict with those that already exist in the drawing. In such cases, the user is given an option to renumber the point numbers from the file, or to cancel the operation which will result with a Visual Basic error. An application that uses ImportPoints should take this into account.
