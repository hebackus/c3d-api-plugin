<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Working with Surfaces > Finding Intersections -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-CE9725EC-9683-4C55-B6ED-C1A7659C37DF.htm -->

# Finding Intersections

When working with surfaces, it can be useful to determine where a vector intersects with a surface, which you can do with the surface’s IntersectPointWithSurface() method. For example, you can determine if the top of a structure is visible from a point on the surface, or whether one point on the surface is visible from another point. This example tests whether a vector starting at (20424.7541, 20518.0409, 100) pointing in direction (0.6, 0.4, -0.5) intersects with the first surface in the drawing, and if it does, it prints out the intersection location:
    
    
    Dim objSurf As AeccSurface
    Dim varStartPt As Variant, varDir As Variant, varIntPt As Variant
    Dim darrStart(2) As Double
    Dim darrDir(2) As Double
    darrStart(0) = 20424.7541
    darrStart(1) = 20518.0409
    darrStart(2) = 100
    darrDir(0) = 0.6
    darrDir(1) = 0.4
    darrDir(2) = -0.5
    varStartPt = darrStart
    varDir = darrDir
    Set objSurf = g_oAeccDoc.Surfaces(0)
    varIntPt = objSurf.IntersectPointWithSurface(varStartPt, varDir)
    If UBound(varIntPt) = 2 Then
       Debug.Print varIntPt(0), varIntPt(1), varIntPt(2)
    End If
