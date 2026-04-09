<!-- Developer's Guide > API Developer's Guide > Alignments > Basic Alignment Operations > Creating an Alignment -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F620DF41-7DF3-450F-8C2A-A92DEB1F9E9E.htm -->

# Creating an Alignment

Alignments are usually created without being associated with an existing site. Each CivilDocument object has its own collection of alignments not associated with a site accessed with the GetSitelessAlignmentIds() method. There is also a collection of all alignments (siteless and associated with a site) accessed with GetAlignmentIds() method. Alignments can be moved into a site with the Alignment.CopyToSite() method. A siteless alignment can be copied from a sited alignment using Alignment.CopyToSite(), and passing ObjectId.Null or ““ as the site.

## Creating a New Alignment

The Alignment class provides versions of the Create() method to create a new Alignment object from a polyline, or without geometry data. There are two overloads for creating an alignment without geometry data. Both take a reference to the document object, and the name of the new alignment. One takes ObjectIds for the site to associate the alignment with (pass ObjectId.Null to create a siteless alignment), the layer to create the alignment on, the style to apply to the alignment, and the label set style to use. The other overload takes strings naming these items. Here’s a simple example that creates a siteless alignment without geometry data:
    
    
    // Uses an existing Alignment Style named "Basic" and Label Set Style named "All Labels" (for example, from
    // the _AutoCAD Civil 3D (Imperial) NCS.dwt template.  This call will fail if the named styles
    // don't exist.  
    // Uses layer 0, and no site (ObjectId.Null)
    ObjectId testAlignmentID = Alignment.Create(doc, "New Alignment", ObjectId.Null, "0", "Basic", "All Labels");
    

There are two overloads of the create() method for creating alignments from polylines. The first takes a reference to the CivilDocument object, a PolylineOptions object (which contains the ID of the polyline to create an alignment from), a name for the new alignment, the ObjectID of a layer to draw to, the ObjectID of an alignment style, and the ObjectID of a label set object, and returns the OjectID of the new Alignment. The second overload takes the same parameters, except the layer, alignment style, and label set are specified by name instead of ObjectID.

This code creates an alignment from a 2D polyline, using existing styles:
    
    
    [CommandMethod("CreateAlignment")]
    public void CreateAlignment()
    {            
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
     
        // Ask the user to select a polyline to convert to an alignment
        PromptEntityOptions opt = new PromptEntityOptions("\nSelect a polyline to convert to an Alignment");
        opt.SetRejectMessage("\nObject must be a polyline.");
        opt.AddAllowedClass(typeof(Polyline), false);
        PromptEntityResult res = ed.GetEntity(opt);
     
        // create some polyline options for creating the new alignment
        PolylineOptions plops = new PolylineOptions();
        plops.AddCurvesBetweenTangents = true;
        plops.EraseExistingEntities = true;
        plops.PlineId = res.ObjectId;
     
        // uses an existing Alignment Style and Label Set Style named "Basic" (for example, from
        // the Civil 3D (Imperial) NCS Base.dwt template.  This call will fail if the named styles
        // don't exist.
        ObjectId testAlignmentID = Alignment.Create(doc, plops, "New Alignment", "0", "Standard", "Standard");
    }
    

## Creating an Alignment Offset From Another Alignment

Alignments can also be created based on the layout of existing alignments. The Alignment::CreateOffsetAlignment() method creates a new alignment with a constant offset and adds it to the same parent site as the original alignment. The new alignment has the same name (followed by a number in parenthesis) and the same style as the original, but it does not inherit any station labels, station equations, or design speeds from the original alignment.
    
    
    [CommandMethod("CreateOffsetAlignment")]
    public void CreateOffsetAlignment()
    {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Ask the user to select an alignment to create a new offset alignment from
            PromptEntityOptions opt = new PromptEntityOptions("\nSelect an Alignment");
            opt.SetRejectMessage("\nObject must be an alignment.");
            opt.AddAllowedClass(typeof(Alignment), false);
            ObjectId alignID = ed.GetEntity(opt).ObjectId;
            Alignment align = ts.GetObject(alignID, OpenMode.ForRead) as Alignment;
     
            // Creates a new alignment with an offset of 10:
            ObjectId offsetAlignmentID = align.CreateOffsetAlignment(10.0);
        }
    }
