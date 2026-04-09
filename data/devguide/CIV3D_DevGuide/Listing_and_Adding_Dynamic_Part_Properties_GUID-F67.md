<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Base Objects > Listing and Adding Dynamic Part Properties -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F679DB76-005F-43AD-BBF4-E84FBAF23C6F.htm -->

# Listing and Adding Dynamic Part Properties

Each type of pipe and structure has many unique attributes (such as size, geometry, design, and composition) that cannot be stored in the standard pipe and structure properties. To give each part appropriate attributes, pipe and structure objects have sets of dynamic properties. A single property is represented by an PartDataField object. Data fields are held in collections of type PartDataRecord. You can reach these collections through the PartData property of the Part class, from which Pipe and Structure objects inherit. Each data field contains an internal variable name, a text description of the value, a global context used to identify the field, data type, and the data value itself, as well as other properties.

This sample enumerates all the data fields contained in a pipe object “oPipe” and displays information from each field.
    
    
    // Get PartDataRecord for first pipe in the network
    ObjectId pipeId =  oNetwork.GetPipeIds()[0];
    Pipe oPipe = ts.GetObject(pipeId, OpenMode.ForRead) as Pipe;
    PartDataField[] oDataFields = oPipe.PartData.GetAllDataFields();
    ed.WriteMessage("Additional info for pipe: {0}\n", oPipe.Name);
    foreach (PartDataField oPartDataField in oDataFields)
    {
        ed.WriteMessage("Name: {0}, Description: {1},  DataType: {2}, Value: {3}\n",
            oPartDataField.Name,
            oPartDataField.Description,
            oPartDataField.DataType,
            oPartDataField.Value); 
    }
    

Dynamic properties created with the NetworkCatalogDef class are not yet supported by the .NET API.
