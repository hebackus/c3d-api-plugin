<!-- Developer's Guide > API Developer's Guide > Profiles > Profiles > Creating a Profile From a Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-3DAFDF1E-BF23-42F0-961D-F3C2DD0541F7.htm -->

# Creating a Profile From a Surface

A profile is an object consisting of elevations along an alignment. Each alignment contains a collection of profiles which you can access by the Alignment.GetProfileIds() method. The Profile.CreateFromSurface() method creates a new profile and derives its elevation information from the specified surface along the path of the alignment. 
    
    
    // Illustrates creating a new profile from a surface
    [CommandMethod("ProfileFromSurface")]
    public void ProfileFromSurface()
    {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Ask the user to select an alignment 
            PromptEntityOptions opt = new PromptEntityOptions("\nSelect an Alignment");
            opt.SetRejectMessage("\nObject must be an alignment.\n");
            opt.AddAllowedClass(typeof(Alignment), true);
            ObjectId alignID = ed.GetEntity(opt).ObjectId;
            // get layer id from the alignment
            Alignment oAlignment = ts.GetObject(alignID, OpenMode.ForRead) as Alignment;
            ObjectId layerId = oAlignment.LayerId;
            // get first surface in the document
            ObjectId surfaceId = doc.GetSurfaceIds()[0];
            // get first style in the document
            ObjectId styleId = doc.Styles.ProfileStyles[0];
            // get the first label set style in the document
            ObjectId labelSetId = doc.Styles.LabelSetStyles.ProfileLabelSetStyles[0];
            try
            {
                ObjectId profileId = Profile.CreateFromSurface("My Profile", alignID, surfaceId, layerId, styleId, labelSetId);
                ts.Commit();
            }
            catch (Autodesk.AutoCAD.Runtime.Exception e)
            {
                ed.WriteMessage(e.Message);
            }
            
        }
    }
