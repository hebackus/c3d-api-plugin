<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Points in COM > Points > Using the Points Collection -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-2636ED24-3FEC-440D-B6B5-B2036373C58F.htm -->

# Using the Points Collection

All points in a document are held in the AeccDocument.Points property, an object of type AeccPoints. Besides the usual collection properties and methods, the Points object also has methods for dealing with large numbers of points at once. An array of positions can be added using the AeccPoints.AddMultiple method. 

The following example adds a series of points to the AeccDocument.Points collection using AddMultiple and then accesses points in the collection directly:
    
    
    ' This adds an array of point locations to the document's
    ' points collection.
    Dim lNumAdded As Long
    Const NUM_LOCATIONS As Long = 3
    ' One dimensional array, 3 for each point location.
    Dim dLocations(0 To (3 * NUM_LOCATIONS) - 1) As Double
    ' One point per line
    dLocations(0) = 4927: dLocations(1) = 3887: dLocations(2) = 150
    dLocations(3) = 5101: dLocations(4) = 3660: dLocations(5) = 250
    dLocations(6) = 5144: dLocations(7) = 3743: dLocations(8) = 350
    lNumAdded = oPoints.AddMultiple(NUM_LOCATIONS, dLocations, 0)
     
    ' This computes the average elevation of all points in a document.
    Dim oPoints As AeccPoints
    Dim i As Long
    Dim avgElevation As Double
    Set oPoints = g_oAeccDocument.Points
    For i = 0 To oPoints.Count - 1
        avgElevation = avgElevation + oPoints.Item(i).Elevation
    Next i
    avgElevation = avgElevation / oPoints.Count
    MsgBox "Average elevation: "& avgElevation & _
      vbNewLine & "Number of points: " & oPoints.Count
