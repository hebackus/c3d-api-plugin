<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies > Getting Applied Subassembly Information -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F2EB3408-2FCA-488B-A965-E20AE8C0A310.htm -->

# Getting Applied Subassembly Information

An applied subassembly consists of a series of calculated shapes, links, and points, represented by objects of type CalculatedShape, CalculatedLink, and CalculatedPoint respectively. 
    
    
    foreach (AppliedSubassembly oSubassembly in oASC)
    {
        ed.WriteMessage("Applied subassembly: Station to baseline: {0}, Offset to baseline: {1}, Elevation to baseline: {2}\n",
            oSubassembly.OriginStationOffsetElevationToBaseline.X,
            oSubassembly.OriginStationOffsetElevationToBaseline.Y,
            oSubassembly.OriginStationOffsetElevationToBaseline.Z);
    }
    

Applied subassemblies also contain an ObjectId reference to the archetype subassembly (of type Subassembly) in the subassembly database. 
    
    
    // Get information about the subassembly template:
    ObjectId oID = oAppliedSubassembly.SubassemblyId;
    Subassembly oSubassembly = ts.GetObject(oID, OpenMode.ForRead) as Subassembly;
    ed.WriteMessage("Subassembly name: {0}\n", oSubassembly.Name);
    

You can access the parameters of an AppliedSubassembly through its Parameters property. The items held in the Parameters collection are of type AppliedSubassemblyParam<T>, depending on the type of the parameter. Use this collection for read access to parameters. To modify the value of a Parameter, use the GetParameter() method, which returns type AppliedSubassemblyParam<T>, depending on the type of the parameter. Defined parameter types are String, Double, Boolean, and Int32. You can check whether a parameter exists with the Contains() method. 

In this example, we look at the first AppliedSubassembly in the first BaselineRegion of a corridor, and print out the type and value for each defined parameter. We also check whether a parameter exists, and change a parameter's value. 
    
    
    string corridorName = "Corridor - (1)";
    // get the CorridorSurface by name:
    ObjectId corridorId = _civildoc.CorridorCollection[corridorName];
    Corridor corridor = ts.GetObject(corridorId, OpenMode.ForRead) as Corridor;
    
    
    // Get the first applied subassembly in the first assembly in the first BaselineRegion:
    BaselineRegion baselineRegion = corridor.Baselines[0].BaselineRegions[0];
    AppliedAssembly appliedAssembly = baselineRegion.AppliedAssemblies[0];
    AppliedSubassembly appliedSubassembly = appliedAssembly.GetAppliedSubassemblies()[0];
                        
    // Get parameter key names:
    foreach (IAppliedSubassemblyParam param in appliedSubassembly.Parameters)
    { _editor.WriteMessage("Parameter key name: {0}\n", param.KeyName); }
    
    foreach (var p in appliedSubassembly.Parameters)
    {
        _editor.WriteMessage("Parameter information: name: {0}, value type: {1}\n", p.KeyName, p.ValueType);
        Object vobj = p.ValueAsObject;
        if (p.ValueType == typeof(System.String))
        { _editor.WriteMessage("Parameter string value: {0}\n", (String)vobj); }
        else if (p.ValueType == typeof(System.Double))
        { _editor.WriteMessage("Parameter double value: {0}\n", (Double)vobj); }
        else if (p.ValueType == typeof(System.Int32))
        { _editor.WriteMessage("Parameter int32 value: {0}\n", (Int32)vobj); }
    else if (p.ValueType == typeof(system.Boolean))
    { editor.WriteMessage(“Parameter bool value: {0}\n”, (Boolean)vobj);}
    
        // we should never get here:
        else { _editor.WriteMessage("Unexpected type.\n"); }
    }
    
    // Check whether a parameter exists 
    Bool result = appliedSubassembly.Contains(“BottomLinkCodes”);
    // Change a parameter’s value
    AppliedSubassemblyParam<string> param = appliedSubassembly.GetParameter<string>("BottomLinkCodes");
    param.Value = "R1S1";
