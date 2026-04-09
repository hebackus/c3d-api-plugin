<!-- Developer's Guide > API Developer's Guide > Profiles > Profile Views > Creating a Profile View -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-2915E081-AAB6-44D7-9111-199BCF8B0093.htm -->

# Creating a Profile View

The ProfileView class has two versions of the ProfileView::Create() method for adding new ProfileView objects to a drawing. Each method overload takes a reference to the CivilDrawing object, the name of the new profile view, and a Point3d location in the drawing where the profile view is inserted. They also both take a band set style and alignment; one version takes these arguments as ObjectIds, while the other takes them as strings. 

This example demonstrates creating a new ProfileView:
    
    
    [CommandMethod("CreateProfileView")]
    public void CreateProfileView()
    {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Ask the user to select an alignment 
            PromptEntityOptions opt = new PromptEntityOptions("\nSelect an Alignment");
            opt.SetRejectMessage("\nObject must be an alignment.\n");
            opt.AddAllowedClass(typeof(Alignment), false);
            ObjectId alignID = ed.GetEntity(opt).ObjectId;
            // Create insertion point:
            Point3d ptInsert = new Point3d(100, 100, 0);
            // Get profile view band set style ID:
            ObjectId pfrVBSStyleId = doc.Styles.ProfileViewBandSetStyles["Standard"];
            // If this doesn't exist, get the first style in the collection
            if (pfrVBSStyleId == null) pfrVBSStyleId = doc.Styles.ProfileViewBandSetStyles[0];
            ObjectId ProfileViewId = ProfileView.Create(doc, "New Profile View", pfrVBSStyleId, alignID, ptInsert);
            ts.Commit();
        }
    }
