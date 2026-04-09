<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces >  Adding and removing Corridor Surfaces -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-D02D2143-716A-4EF6-8249-7F4B48EED0FC.htm -->

#  Adding and removing Corridor Surfaces

The CorridorSurfaceCollection object allows you to add a new, empty CorridorSurface with the Add() method. This method takes a string specifying the new CorridorSurface name, and an optional StyleID of a CorridorSurfaceStyle to apply to the surface. 

CorridorSurfaces may be removed from the CorridorSurfaceCollection using either the Remove() or RemoveAt() methods. Remove() takes a string specifying the CorridorSurface name, or a CorridorSurface object itself. RemoveAt() takes an integer specifying the index of the CorridorSurface object in the CorridorSurfaceCollection to remove. 

This example illustrates creating a new CorridorSurface and adding it to the CorridorSurfaces collection on a specified Corridor. 
    
    
    // prompt for the target corridor name:
    String corridorName = _editor.GetString("Enter a corridor name:").StringResult;
    // Get the corridor
    ObjectId corridorId = _civilDoc.CorridorCollection[corridorName];
    Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;
    
    // Get a surface style to use for the new corridor surface:
    ObjectId surfaceStyleId = _civilDoc.Styles.SurfaceStyles[0];
    CorridorSurface corridorSurface = corridor.CorridorSurfaces.Add("New Example Corridor Surface", surfaceStyleId);
    
    // Corridor will now be out-of-date:
    _editor.WriteMessage("Corridor is out of date: {0}", corridor.IsOutOfDate);
    // You can re-build, although this won't do anything in this case, since
    // the new surface is empty:
    corridor.Rebuild();
    
    
    // Remove the new surface:
    corridor.CorridorSurfaces.Remove(corridorSurface);
    
    ts.Commit();
