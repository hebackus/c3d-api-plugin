<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies > Creating Assemblies -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-96A793AE-760D-4659-A480-E8A4A2C17793.htm -->

# Creating Assemblies

Assemblies can be created in a CivilDocument with the AssemblyCollection.Add() method. This method takes the name of the newly created Assembly, the Assembly type (using the AssemblyType enum), and the Point3d location in the drawing to insert the new Assembly. You can optionally specify the ObjectId of the AssemblyStyle and CodeSetStyle to apply to the Assembly. 

In the sample below, a new, empty Assembly is created in the CivilDocument's AssemblyCollection using a Point3d entered by the user. 
    
    
    // Add a new assembly
    Point3d location = _editor.GetPoint("Select assembly location").Value;
    ObjectId assemblyId = _civilDoc.AssemblyCollection.Add("New Assembly", AssemblyType.DividedPlanarRoad, location);
    Assembly assembly = ts.GetObject(assemblyId, OpenMode.ForWrite) as Assembly;
