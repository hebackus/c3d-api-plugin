<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies >  Working with Subassemblies in an Assembly -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9A86FF91-547D-4843-8D5D-F28201EF836B.htm -->

#  Working with Subassemblies in an Assembly

The Assembly object exposes several methods for working with its component Subassemblies. There are methods for adding, copying, inserting, mirroring, and replacing Subassemblies. 

In this example, a stock subassembly is imported, then added to a drawing Assembly object, then mirrored: 
    
    
    // Add stock subassembly to drawing
    ObjectId subassemblyId = _civildoc.SubassemblyCollection.ImportStockSubassembly("Imported subassembly", "Subassembly.BasicLane", offsetLocation);
    
    // Add stock subassembly to assembly
    AssemblyGroup assemblyGroup = assembly.AddSubassembly(subassemblyId);
    
    // mirror subassembly
    AssemblyGroup mirrorAssemblyGroup = assembly.MirrorSubassembly(subassemblyId);
