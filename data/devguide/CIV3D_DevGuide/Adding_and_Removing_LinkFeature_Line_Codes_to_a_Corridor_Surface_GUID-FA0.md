<!-- Developer's Guide > API Developer's Guide > Corridors > Corridor Surfaces > Adding and Removing Link/Feature Line Codes to a Corridor Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-FA0224D5-8047-460F-A235-E1C7ABF40C31.htm -->

# Adding and Removing Link/Feature Line Codes to a Corridor Surface

You can modify a CorridorSurface object by adding or removing the link codes and feature line codes that define the surface. Link codes are added with the AddLinkCode() method, and feature line codes are added with the AddFeatureLineCode() method. They are removed with RemoveLinkCode() and RemoveFeatureLineCode() respectively. All these methods take a string containing the code name. 

In the example below, the user is prompted to enter a link and feature line code name, and these codes are added, and then removed from the CorridorSurface definition. If the specified code name does not exist, a System.ArgumentException is thrown. No exception is thrown if the code already exists in the CorridorSurface definition. 
    
    
    string corridorSurfaceName = "Corridor - (1) Top";
    string corridorName = "Corridor - (1)";
    // get the CorridorSurface by name:
    ObjectId corridorId = _civilDoc.CorridorCollection[corridorName];
    Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;
    CorridorSurface corridorSurface = corridor.CorridorSurfaces[corridorSurfaceName];
    
    // get a featureline name and link code:
    string linkCodeName = _editor.GetString("Enter a link code: ").StringResult;
    string featureLineName = _editor.GetString("Enter a feature line code: ").StringResult;
    try
    {
        corridorSurface.AddLinkCode(linkCodeName, true);
                        
        // The new code will be listed here
        string[] linkCodes = corridorSurface.LinkCodes();
        _editor.WriteMessage("Link codes in corridor surface: \n  {0}", String.Join("  \n", linkCodes));
    
        corridorSurface.AddFeatureLineCode(featureLineName);
        string[] featureLineCodes = corridorSurface.FeatureLineCodes();
        _editor.WriteMessage("Link codes in corridor surface: \n  {0}", String.Join("  \n", featureLineCodes));
    
        // remove the new items
        corridorSurface.RemoveFeatureLineCode(featureLineName);
        corridorSurface.RemoveLinkCode(linkCodeName);
    
    }
    
    // if either code does not exist, this will be thrown:
    catch (System.ArgumentException e)
    {
        _editor.WriteMessage(e.ToString());
    }
