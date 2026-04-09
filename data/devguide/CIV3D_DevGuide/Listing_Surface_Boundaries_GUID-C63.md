<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces > Listing Surface Boundaries -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C631999D-AB2C-4419-A1E7-2EFE485715B2.htm -->

# Listing Surface Boundaries

Two different objects are used to define the limits of a corridor surface: boundaries and masks. A boundary is a polygon representing the outer edge of a surface or the inside edge of a hole in a surface. A mask is a polygon representing the part of the surface that can be displayed. The collection of all the boundaries of a surface are stored in the CorridorSurface.Boundaries property and the collection of all masks are stored in the CorridorSurface.Masks property. 

Boundaries (of type CorridorSurfaceBoundary) and masks (of type CorridorSurfaceMask) are both derived from the same base class (CorridorSurfaceBaseMask) and both have similar methods and properties. The array of points making up the border polygon is retrieved by calling the PolygonPoints() method. If the border was originally defined by selecting segments of feature lines, the collection of all such feature line components are contained in the FeatureLineComponents property. 

See [Modifying Suface Boundaries](<GUID-FF66838C-91AD-4248-A365-FCD1F62337EE.htm>) for information about how to modify Corridor surface boundaries and masks. 

This sample loops through all the boundaries of a corridor surface and displays information about each: 
    
    
    // List boundaries
    foreach (CorridorSurfaceBoundary oCorridorSurfaceBoundary in oCorridorSurface.Boundaries)
    {
        if (oCorridorSurfaceBoundary.BoundaryType == CorridorSurfaceBoundaryType.InsideBoundary)
            ed.WriteMessage("Inner Boundary: ");
        else
            ed.WriteMessage("Outer Boundary: ");
     
        ed.WriteMessage(oCorridorSurfaceBoundary.Name);
     
        // Get the points of the boundary polygon
        Point3d[] oPoints = oCorridorSurfaceBoundary.PolygonPoints();
        ed.WriteMessage("\nNumber of points: {0}\n", oPoints.Length);
        // Print the location of the first point. Usually corridors
        // have a large number of boundary points, so we will not
        // bother printing all of them.
        ed.WriteMessage("Point 1: {0},{1},{2}\n",
            oPoints[0][0],
            oPoints[0][1],
            oPoints[0][2]);
     
        // Display information about each feature
        // line component in this surface boundary.
        ed.WriteMessage("Feature line components \n Count: {0}\n",
            oCorridorSurfaceBoundary.FeatureLineComponents.Count);
     
        foreach (FeatureLineComponent oFeatureLineComponent in oCorridorSurfaceBoundary.FeatureLineComponents)
        {
            ed.WriteMessage("Code: {0}, Start station: {1}, End station: {2}\n",
                oFeatureLineComponent.FeatureLine.CodeName,
                oFeatureLineComponent.StartStation,
                oFeatureLineComponent.EndStation);
        }
    }
