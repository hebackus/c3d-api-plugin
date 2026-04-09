<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with Surfaces > Adding a Boundary -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4AD08174-038B-4598-9765-B57208F7FA50.htm -->

# Adding a Boundary

A boundary is a closed polyline that defines the visibility of surface triangles within it. A boundary can hide all triangles outside it, hide all triangles inside it, or show triangles inside it that would otherwise be hidden. Boundaries also change surface statistics such as area and number of triangles. Boundaries can either be “destructive” (totally hiding triangles that cross the boundary) or “non-destructive” (clipping triangle edges at the point where they cross the boundary). Normally, TIN surfaces use non-destructive boundaries, while grid surfaces can only have destructive boundaries:

Non-destructive Boundary

All boundaries applied to a surface are stored in the AeccSurface.Boundaries collection. The boundary itself is defined by an AutoCAD entity such as a closed POLYLINE or POLYGON. The height of the entity plays no part in how surface triangles are clipped, so you can use 2D entities. This entity can also contain curves, but the boundary always consists of lines. How these lines are tessellated is defined by the mid-ordinate distance, which is the maximum distance between a curve and the lines that are generated to approximate it:

Mid-ordinate Distance

This sample adds a square outside boundary to a surface:
    
    
    ' First we need an AutoCAD entity (in this case a polyline)
    ' which describes the boundary location.
    Dim oPoly As AcadPolyline
    Dim dPoints(0 To 11) As Double
    dPoints(0) = 1000: dPoints(1) = 1000: dPoints(2) = 0
    dPoints(3) = 1000: dPoints(4) = 4000: dPoints(5) = 0
    dPoints(6) = 4000: dPoints(7) = 4000: dPoints(8) = 0
    dPoints(9) = 4000: dPoints(10) = 1000: dPoints(11) = 0
    Set oPoly = oAeccDocument.Database.ModelSpace _
      .AddPolyline(dPoints)
    oPoly.Closed = True
     
    ' The name of the boundary object.
    Dim sName as String
    sName = "Sample Boundary"
    ' The third parameter describes what the boundary does
    ' to triangles inside it. The fourth parameter is True
    ' if you want non-destructive boundary or false otherwise.
    ' The final parameter is the mid-ordinate distance.
    Dim oNewBoundary As AeccSurfaceBoundary
    Set oNewBoundary = oSurface.Boundaries.Add(oPoly, sName, _
      aeccBoundaryOuter, True, 10.5)
    

Note:

Any operation that causes the formation of new triangles (such as adding points or breaklines to a TIN surface) may result in triangles that cross existing boundary lines. Boundaries should always be added after every other operation that adds points to a surface.
