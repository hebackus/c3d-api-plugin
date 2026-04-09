<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Corridor Surfaces > Listing Surface Boundaries -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-0EFBE387-A5A1-48B7-830C-D45F25C8FC16.htm -->

# Listing Surface Boundaries

Two different objects are used to define the limits of a corridor surface: boundaries and masks. A boundary is a polygon representing the outer edge of a surface or the inside edge of a hole in a surface. A mask is a polygon representing the part of the surface that can be displayed. The collection of all the boundaries of a surface are stored in the AeccCorridorSurface.Boundaries property and the collection of all masks are stored in the AeccCorridorSurface.Masks property. 

Boundaries (of type AeccCorridorSurfaceBoundary) and masks (of type AeccCorridorSurfaceMask) are both derived from the same base interface (IAeccCorridorSurfaceBaseMask) and both have the similar methods and properties. The array of points making up the border polygon is retrieved by calling the GetPolygonPoints method. If the border was originally defined by selecting segments of feature lines, the collection of all such feature line components are contained in the FeatureLineComponents property.

Note:

The Autodesk Civil 3D API does not include methods for creating or modifying corridor boundaries or masks.

This sample loops through all the boundaries of a corridor surface and displays information about each:
    
    
    Dim oCSBoundary As AeccCorridorSurfaceBoundary
     
    For Each oCSBoundary In oCorridorSurface.Boundaries
       ' Get the type of boundary.
       Dim sBoundaryTitle As String
       If (oCSBoundary.Type = aeccCorridorSurfaceInsideBoundary) Then
          sBoundaryTitle = "  Inner Boundary: "
       Else
          sBoundaryTitle = "  Outer Boundary: "
       End If
       Debug.Print sBoundaryTitle & oCSBoundary.Name
     
       ' Get the points of the boundary polygon.
       Dim vPoints As Variant
       vPoints = oCSBoundary.GetPolygonPoints()
       Debug.Print " " & UBound(vPoints) & " points" 
       ' Print the location of the first point. Usually corridors
       ' have a large number of boundary points, so we will not
       ' bother printing all of them.
       X = vPoints(1)(0)
       Y = vPoints(1)(1)
       Z = vPoints(1)(2)
       Debug.Print "Point 1: "; X; ", "; Y; ", "; Z
     
       ' Display information about each feature
       ' line component in this surface boundary.
       Debug.Print 
       Debug.Print "Feature line components"
       Debug.Print " Count: "; 
       Debug.Print oCSBoundary.FeatureLineComponents.Count
     
       Dim oFeatureLineComponent As AeccFeatureLineComponent
       For Each oFLineComponent In oCSBoundary.FeatureLineComponents
          Debug.Print "Code:" & oFLineComponent.FeatureLine.CodeName
          Debug.Print "Start station:" & oFLineComponent.StartStation
          Debug.Print "End station:" & oFLineComponent.EndStation
          Debug.Print: Debug.Print
       Next ' Feature line components
    Next ' Corridor surface boundaries
