<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces >  Creating a Surface from a Corridor Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-BD073453-C094-4F6D-B95B-D01402FC10BD.htm -->

#  Creating a Surface from a Corridor Surface

When you create a CorridorSurface, a linked Surface with the same name is created in the document's collection of surfaces. However, because this Surface is an output of the corridor model, it is dynamically linked to the CorridorSurface, and if the CorridorSurface is removed, the related Surface is as well. To create an independent Surface object from a CorridorSurface, you can use the TinSurface.CreateFromCorridorSurface() method, which is analogous to exporting a surface in the UI using the "Create Surface From Corridor" command. This static method takes the name to assign the new, independent surface, and a reference to a CorridorSurface object to create the new surface from. 

In the example below, a new Surface is created from a CorridorSurface, and then the source CorridorSurface is removed. However, the count of Surfaces in the document stays the same before and after the removal, showing that the independent Surface is not removed. 
    
    
    string corridorSurfaceName = "Corridor - (1) Top";
    string corridorName = "Corridor - (1)";
    
    // get the CorridorSurface by name:
    ObjectId corridorId = _civilDoc.CorridorCollection[corridorName];
    Corridor corridor = ts.GetObject(corridorId, OpenMode.ForWrite) as Corridor;
    CorridorSurface corridorSurface = corridor.CorridorSurfaces[corridorSurfaceName];
    
    // Count the number of surfaces:
    _editor.WriteMessage("# of existing surfaces: {0}\n", _civilDoc.GetSurfaceIds().Count);
    ObjectId surfaceId = TinSurface.CreateFromCorridorSurface("New Surface", corridorSurface);
    
    corridor.CorridorSurfaces.Remove(corridorSurface);
    
    // Even though the CorridorSurface is removed, surface count remains the same:
    _editor.WriteMessage("# of existing surfaces after CorridorSurface removal: {0}\n", _civilDoc.GetSurfaceIds().Count);
