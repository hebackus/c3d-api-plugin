<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies > Working with Assembly Groups -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DD4C3865-E531-42D2-8C5A-E86495472951.htm -->

# Working with Assembly Groups

The Subassemblies in an Assembly object are organized in groups. These AssemblyGroup objects are accessed via the Assembly.Groups property, while offset AssemblyGroup objects are accessed via the OffsetAssembly.Groups property. All Subassembly objects in an AssemblyGroup or offset AssemblyGroup are accessed by the parent AssemblyGroup or offset AssemblyGroup object's GetSubassemblyIds() method, which returns an ObjectIdCollection containing the ObjectIds of all the Subassembly objects in the AssemblyGroup or offset AssemblyGroup.

In this example, each AssemblyGroup and Subassembly in each AssemblyGroup for a specified Assembly are listed in the editor. 
    
    
    // Assembly
    // Get an Assembly by name:
    ObjectId assemblyId2 = _civilDoc.AssemblyCollection["Assembly - (1)"];
    Assembly assembly2 = ts.GetObject(assemblyId2, OpenMode.ForRead) as Assembly;
    _editor.WriteMessage("Assembly name: {0}\n", assembly2.Name);
    foreach (AssemblyGroup assemblyGroup2 in assembly2.Groups)
    {
        _editor.WriteMessage("Subassemblies in Group {0}:\n", assemblyGroup2.Name);
        foreach (ObjectId subassemblyid2 in assemblyGroup2.GetSubassemblyIds())
        {
            Subassembly subassembly2 = ts.GetObject(subassemblyid2, OpenMode.ForRead) as Subassembly;
            _editor.WriteMessage("Subassembly: {0}\n", subassembly2.Name);
        }
    }
    
    // OffsetAssembly
    OffsetAssemblyCollection OffsetAssemblies = assembly2.OffsetAssemblies;
    OffsetAssembly offsetAssembly = OffsetAssemblies[0];
    _editor.WriteMessage("Offset assembly name: {0}\n", offsetAssembly.Name);
    foreach (AssemblyGroup offsetAssemblyGroup in offsetAssembly.Groups)
    {
        _editor.WriteMessage("Subassemblies in Offset Group {0}:\n", offsetAssembly.Name);
        foreach (ObjectId subassemblyid in offsetAssemblyGroup.GetSubassemblyIds())
        {
            Subassembly subassembly = ts.GetObject(subassemblyid, OpenMode.ForRead) as Subassembly;
            _editor.WriteMessage("Subassembly: {0}\n", subassembly.Name);
        }
    }
