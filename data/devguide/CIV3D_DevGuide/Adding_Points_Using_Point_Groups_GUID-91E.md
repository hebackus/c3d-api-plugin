<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with TIN Surfaces > Adding Point Data to a TIN Surface > Adding Points Using Point Groups -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-91E824D9-9E04-4FA6-8E6F-F817932FBECC.htm -->

# Adding Points Using Point Groups

You can manually add points to a TIN surface by adding point groups to the AeccTinSurface.PointGroups collection.
    
    
    ' Make a surface consisting of 30 random points. To do
    ' this, first add 30 points to the document's collection
    ' of points, then make a point group from those points. 
    ' Finally, add that point group to the surface.
    Dim i As Integer
    For i = 0 To 29
        Dim pt(0 To 2) As Double
        pt(0) = Int(5000 * Rnd())
        pt(1) = Int(5000 * Rnd())
        pt(2) = Int(200 * Rnd())
        Dim oPoint As AeccPoint
        Set oPoint = oAeccDocument.Points.Add(pt)
        oPoint.Name = "Point" & CStr(i)
    Next i
     
    Dim oPtGroup As AeccPointGroup
    Set oPtGroup = oAeccDocument.PointtGroups.Add("Random group")
    ' Add all points with a name beginning with "Point"
    oPtGroup.QueryBuilder.IncludeNames = "point*"
    ' Add the point group to the surface.
    oTinSurface.PointGroups.Add oPtGroup
    oTinSurface.Update
    

You can also add points to a surface by adding contour lines. See [Adding Contours to a TIN Surface](<GUID-75295A16-B6C0-4C11-8A35-7824DD28489B.htm>).

All points that make up a surface can be retrieved from the read-only AeccTinSurface.Points property, which is an array of locations.
    
    
    ' Print the location (easting, northing, and elevation)
    ' of the 1000th point.
    Dim vLocation as Variant
    vLocation = oTinSurface.Points(1000)
     
    ' Now vLocation contains a 3 element array of doubles.
    Debug.Print "Easting:"; vLocation(0)
    Debug.Print "Northing:"; vLocation(1)
    Debug.Print "Elevation:"; vLocation(2)
