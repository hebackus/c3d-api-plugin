<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces >  Adding and Removing Corridor Surface Masks -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-15E739C2-2A72-49E9-9391-789CAA5A1D51.htm -->

#  Adding and Removing Corridor Surface Masks

The CorridorSurface.Masks property exposes the collection of masks associated with the CorridorSurface as an object of type CorridorSurfaceMaskCollection. This object allows you to add and remove masks from the CorridorSurface object. Masks may be added from a polyline, a Point3dCollection, or a feature line code. You may also add a new, empty mask. Masks may be removed from the collection by name, or by CorridorSurfaceMask object, or by index using the RemoveAt() method. 

In the sample below, several new surface masks are added to the collection using different methods, and one is removed by direct reference: 
    
    
    string corridorSurfaceName = "Corridor - (1) Top";
    string corridorName = "Corridor - (1)";
    
    // get the CorridorSurface by name:
    ObjectId corridorId = _civilDoc.CorridorCollection[corridorName];
    Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;
    CorridorSurface corridorSurface = corridor.CorridorSurfaces[corridorSurfaceName];
    
    _editor.WriteMessage("# of masks in corridor surface: " +  corridorSurface.Masks.Count);
    CorridorSurfaceMask corridorSurfaceMask = corridorSurface.Masks.Add("New Empty Mask");
    
    ObjectId polyLineId= promptForObjectType("Select a polyline to add as a mask", typeof(Polyline));
    corridorSurface.Masks.Add("New mask from polyline", polyLineId);
    
    string codeName = "Daylight_Cut";
    corridorSurface.Masks.Add               ("New mask from feature code", codeName);
    
    _editor.WriteMessage("# of masks in corridor surface: " + corridorSurface.Masks.Count);
    
    // remove the empty mask:
    corridorSurface.Masks.Remove(corridorSurfaceMask);
