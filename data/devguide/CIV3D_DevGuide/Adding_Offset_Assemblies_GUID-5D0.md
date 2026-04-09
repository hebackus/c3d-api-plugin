<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies > Adding Offset Assemblies -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5D05F7C0-8F97-4701-9ED9-F82DD44E4004.htm -->

# Adding Offset Assemblies

Offset Assemblies are contained in an Assembly object's OffsetAssemblies collection, and can be added using the Add() method. This method takes the name of the new Offset Assembly, and an offset from the Assembly as a Vector2d object. 

In the sample below, a new Offset Assembly is created and added to an Assembly object's OffsetAssemblies collection. 
    
    
    // Add offset assembly
    Point3d offsetLocation = _editor.GetPoint("Select offset assembly location").Value;
    Point2d location2d = new Point2d(location.X, location.Y);
    Point2d offsetLocation2d = new Point2d(offsetLocation.X, offsetLocation.Y);
    Vector2d offset = offsetLocation2d - location2d;
    assembly.OffsetAssemblies.Add("New Offset Assembly", offset);
