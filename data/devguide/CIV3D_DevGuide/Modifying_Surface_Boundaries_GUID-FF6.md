<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces > Modifying Surface Boundaries -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FF66838C-91AD-4248-A365-FCD1F62337EE.htm -->

# Modifying Surface Boundaries

Some properties of CorridorSurfaceBoundary objects can be modified after the boundary is added or created. The polygon points for all types of CorridorSurfaceBoundary objects are read-only. However, the feature line components of CorrdiorSurfaceBoundary objects defined by feature lines can be modified. Other properties for both types of CorridorSurfaceBoundaries may be modified, such as the Name, and Description. The BoundaryType cannot be modified. 

The example below illustrates setting modifying some of the properties of an existing CorridorSurfaceBoundary: 
    
    
    string corridorName = "Corridor - (1)";
    string corridorSurfaceName = "Corridor - (1) Top";
    string boundaryName = "Corridor Boundary(1)";
    
    // With surface name, find surface and associated corridor ID
    Corridor corridor = ts.GetObject( _civilDoc.CorridorCollection[corridorName], OpenMode.ForWrite) as Corridor;
    CorridorSurface corridorSurface = corridor.CorridorSurfaces[corridorSurfaceName];
    // Get a boundary
                     
    CorridorSurfaceBoundary corridorSurfaceBoundary = corridorSurface.Boundaries[boundaryName];
    corridorSurfaceBoundary.Description = "A modified description";
    corridorSurfaceBoundary.Name = "A modified boundary name";
