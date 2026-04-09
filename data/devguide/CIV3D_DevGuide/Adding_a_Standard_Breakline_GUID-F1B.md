<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with TIN Surfaces > Adding a Breakline to a TIN Surface > Adding a Standard Breakline -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F1BD404C-4E0B-4B2D-B3C3-7F964A69C644.htm -->

# Adding a Standard Breakline

A standard breakline consists of an array of 3D lines or polylines. Each line endpoint becomes a point in the surface and surface triangles around the breakline are redone. If the polyline contains curves, then the curve is tessellated based on the mid-ordinate distance parameter.
    
    
    ' Create the polyline basis for the breakline.
    Dim o3DPoly as Acad3DPolyline
    Dim dPoints(0 To 8) As Double
    dPoints(0) = 1200: dPoints(1) = 1200: dPoints(2) = 150
    dPoints(3) = 2000: dPoints(4) = 3000: dPoints(5) = 120
    dPoints(6) = 3000: dPoints(7) = 2000: dPoints(8) = 100
    Set o3DPoly = oAeccDocument.Database.ModelSpace _ 
      .Add3DPoly(dPoints)
    o3DPoly.Closed = False
    Dim oBreakline As AeccSurfaceBreakline
    Dim vBLines As Variant
    ' This has to be an array, even if we only have one entity.
    Dim oEntityArray(0) As AcadEntity
    Set oEntityArray(0) = oAeccDocument.Database.ModelSpace _
      .Add3DPoly(dPoints)
    Set oBreakline = oTinSurface.Breaklines.AddStandardBreakline _
      (oEntityArray, "Sample Standard Break", 1#)
