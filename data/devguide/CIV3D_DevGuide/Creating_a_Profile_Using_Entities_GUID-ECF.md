<!-- Developer's Guide > API Developer's Guide > Profiles > Profiles > Creating a Profile Using Entities -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-ECFE15EE-9F18-4F18-A315-D4B51766E95E.htm -->

# Creating a Profile Using Entities

The various Profile.CreateByLayout() overloaded methods create a new profile with no elevation information. The vertical shape of a profile can then be specified using entities. Entities are geometric elements - tangents or symmetric parabolas. The collection of all entities that make up a profile are contained in the Profile.Entities collection. The ProfileEntityCollection class also contains all the methods for creating new entities.

This sample creates a new profile along the alignment “oAlignment” and then adds three entities to define the profile shape. Two straight entities are added at each end and a symmetric parabola is added in the center to join them and represent the sag of a valley.
    
    
    // Illustrates creating a new profile without elevation data, then adding the elevation
    // via the entities collection
     
    [CommandMethod("CreateProfileNoSurface")]
    public void CreateProfileNoSurface()
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
     
            Alignment oAlignment = ts.GetObject(alignID, OpenMode.ForRead) as Alignment;
     
            // use the same layer as the alignment
            ObjectId layerId = oAlignment.LayerId;
            // get the standard style and label set 
            // these calls will fail on templates without a style named "Standard"
            ObjectId styleId = doc.Styles.ProfileStyles["Standard"];
            ObjectId labelSetId = doc.Styles.LabelSetStyles.ProfileLabelSetStyles["Standard"];
     
            ObjectId oProfileId = Profile.CreateByLayout("My Profile", alignID, layerId, styleId, labelSetId);
     
            // Now add the entities that define the profile.
     
            Profile oProfile = ts.GetObject(oProfileId, OpenMode.ForRead) as Profile;
     
            Point3d startPoint = new Point3d(oAlignment.StartingStation, -40, 0);
            Point3d endPoint = new Point3d(758.2, -70, 0);
            ProfileTangent oTangent1 = oProfile.Entities.AddFixedTangent(startPoint, endPoint);
     
            startPoint = new Point3d(1508.2, -60.0, 0);
            endPoint = new Point3d(oAlignment.EndingStation, -4.0, 0);
            ProfileTangent oTangent2 =oProfile.Entities.AddFixedTangent(startPoint, endPoint);
     
            oProfile.Entities.AddFreeSymmetricParabolaByLength(oTangent1.EntityId, oTangent2.EntityId, VerticalCurveType.Sag, 900.1, true);
     
            ts.Commit();
        }
     
    }
