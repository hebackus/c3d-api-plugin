<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces > Creating CorridorSurface Boundaries -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6D3E71CC-E762-4B5C-A781-E8508FBD0C78.htm -->

# Creating CorridorSurface Boundaries

There are several ways to add a new boundary to a CorridorSurface, using versions of the CorridorSurfaceBoundaryCollection.Add() method. This method allows you to add a new boundary in several ways: 

  1. \- As a new, empty boundary; 
  2. \- From a polyline; 
  3. \- From a collection of Point3d objects; 
  4. \- From a feature line. 

You can also add a new outer boundary using AddCorridorExtentsBoundary(). This method corresponds to adding a new boundary using the "Corridor Extents As Outer Boundary" command in the UI. 

You can also examine existing boundaries to determine how they were created. Outer boundaries created with AddCorridorExtentsBoundary() have the IsCorridorExtents property set to true, while boundaries created from polylines and Point3d collections have the IsDefinedFromPolygon set to true. 

In the code sample below, we prompt for a corridor surface name, and then add three types of boundary to its Boundaries collection: an empty boundary defined by corridor extents, an outer boundary, and a boundary from a polyline. 
    
    
    Corridor corridor = null;
    CorridorSurface corridorSurface = null;
    
    string surfaceName = _editor.GetString("Enter Corridor Surface name: ").StringResult;
    // With surface name, find surface and associated corridor ID
    foreach (ObjectId oid in _civilDoc.CorridorCollection)
    {
        Corridor c = ts.GetObject(oid, OpenMode.ForWrite) as Corridor;
        if (c.CorridorSurfaces[surfaceName] != null)
        {
            // this is the matching surface and corridor
            corridor = c;
            corridorSurface = c.CorridorSurfaces[surfaceName];
    	break;
        }
    }
    
    // add outer boundary:
    CorridorSurfaceBoundary outerBoundary = corridorSurface.Boundaries. AddCorridorExtentsBoundary("OuterBoundary");
    
    _editor.WriteMessage("New outer boundary has {0} polygon points.", outerBoundary.PolygonPoints().Length);
    
    // add empty boundary:
    CorridorSurfaceBoundary emptyBoundary = corridorSurface.Boundaries.Add("EmptyBoundary");
    
    // prompt for polyline to add as boundary:
    ObjectId polylineId = promptForObjectType("Select a polyline to add to the surface boundary collection:", typeof(Polyline));
    CorridorSurfaceBoundary polyBoundary = corridorSurface.Boundaries.Add("Polyline boundary", polylineId);
    
    ts.Commit();
