<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces > Computing Cut and Fill  -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-66C13340-084E-4151-B016-48DA6EA41BFD.htm -->

# Computing Cut and Fill 

One important use of corridor surfaces is to compare them against an existing ground surface to determine the amounts of cut and fill required to shape the terrain to match the proposed corridor. 

This sample code demonstrates the creation of a volume surface from the difference between the existing ground and the datum surface of a corridor to determine cut, fill, and volume statistics. Note that the comparison TinVolumeSurface is not created directly from the CorridorSurface, but from the corresponding Surface in the CivilDocument surfaces collection (obtained with getSurfaceIds()) that shares the same name. 
    
    
    string baseSurfaceName = "EG";
     string corridorSurfaceName = "Corridor - (1) Top";
     string corridorName = "Corridor - (1)";
    
     // get the CorridorSurface by name:
     ObjectId corridorId = _civilDoc.CorridorCollection[corridorName];
     Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;
     CorridorSurface corridorSurface = corridor.CorridorSurfaces[corridorSurfaceName];
    
     // Get the oid of both the base surface and the drawing surface corresponding to the
     // corridor surface:
     ObjectId baseId = ObjectId.Null;
     ObjectId corridorSurfaceId = ObjectId.Null;
     foreach (ObjectId oid in _civilDoc.GetSurfaceIds())
     {
    Surface surface = ts.GetObject(oid, OpenMode.ForRead) as Surface;
    if (surface.Name == baseSurfaceName) baseId = oid;
    if (surface.Name == corridorSurfaceName) corridorSurfaceId = oid;
     }
    
    
    
     // Create TinVolumeSurface from which to obtain cut and fill analysis:
      ObjectId compareSurfaceId = TinVolumeSurface.Create("Corridor Cut And Fill", baseId, corridorSurfaceId);
      TinVolumeSurface compareSurface = ts.GetObject(compareSurfaceId, OpenMode.ForNotify) as TinVolumeSurface;
     VolumeSurfaceProperties volumeSurfaceProperties = compareSurface.GetVolumeProperties();
     _editor.WriteMessage("Cut and fill analysis: \n Cut: {0} \n Fill: {1}\n Net: {2}\n", volumeSurfaceProperties.AdjustedCutVolume, volumeSurfaceProperties.AdjustedFillVolume, volumeSurfaceProperties.AdjustedNetVolume);
