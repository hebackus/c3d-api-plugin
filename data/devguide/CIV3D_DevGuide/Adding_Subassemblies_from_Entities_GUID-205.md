<!-- Developer's Guide > API Developer's Guide > Corridors > Assemblies and Subassemblies >  Adding Subassemblies from Entities -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-2059B86E-4E96-4564-814F-0B580962BD12.htm -->

#  Adding Subassemblies from Entities

Subassembly objects may be added to the document's collection of Subassemblies from an entity using the CivilDocument.SubassemblyCollection's Add() method. Valid entity types that can be used to create subassembly are Polyline, Polyline3d, Polyline2d, Feature, Face, Line, Circle, Arc, Ellipse and Spline objects. This method takes the name of the new Subassembly object (a string), the ObjectId of an AutoCAD entity, the mid-ordinate distance for tessellating curves (if it has any), and a LinkCreationType enum to specify link creation behaviour for the Subassembly. For more information about these options, see the "Creating Subassemblies from Polylines" section of the Civil 3D User's Guide. 

In this example, a new subassembly is created from a polyline selected by the user, then the Subassembly collection is iterated: 
    
    
    ObjectId polylineId = promptForEntity("Select a polyline to add as a subassembly.\n", typeof(Polyline));
    SubassemblyCollection subassemblyCollection = _civildoc.SubassemblyCollection;
    ObjectId newSubassemblyId = subassemblyCollection.Add("New Subassembly", polylineId, 1.0, LinkCreationType.Single);
    
    // iterate through all subassemblies, and show the new subassembly in the collection:
    foreach (ObjectId saId in _civildoc.SubassemblyCollection)
    {
        Subassembly sa = ts.GetObject(saId, OpenMode.ForRead) as Subassembly;
        _editor.WriteMessage("Subassembly : {0}\n", sa.Name);
    }
