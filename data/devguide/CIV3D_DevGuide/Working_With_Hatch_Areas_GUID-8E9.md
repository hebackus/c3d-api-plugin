<!-- Developer's Guide > API Developer's Guide > Profiles > Profile Views > Setting Profile View Styles > Working With Hatch Areas -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8E9CA603-DDF7-44F1-8CEF-0193781A352E.htm -->

# Working With Hatch Areas

Hatch areas are a feature of profile views that apply a style to areas of cut and fill to highlight them. In addition to cut and fill, a hatch area can highlight areas of intersection between any two defined profiles. 

The hatching feature for ProfileView objects is exposed by the HatchAreas property. This is a collection of all ProfileHatchArea objects defined for the ProfileView, which can be used to access or add additional hatch areas. 

Each ProfileHatchArea has a set of criteria (ProfileCriteria objects) that specify the profile that defines the upper or lower boundary for the hatch area. The criteria also references a ShapeStyle object that defines how the hatch area is styled in the profile view.

This code sample illustrates how to access the hatch areas for a profile view, and prints out some information about each ProfileHatchArea object’s criteria:
    
    
    [CommandMethod("ProfileHatching")]
    public void ProfileHatching () {
        doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using ( Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction() ) {
            // Ask the user to select a profile view 
            PromptEntityOptions opt = new PromptEntityOptions("\nSelect a profile view");
            opt.SetRejectMessage("\nObject must be a profile view.\n");
            opt.AddAllowedClass(typeof(ProfileView), false);
            ObjectId profileViewID = ed.GetEntity(opt).ObjectId;
            ProfileView oProfileView = ts.GetObject(profileViewID, OpenMode.ForRead) as ProfileView;
            ed.WriteMessage("\nHatch areas defined in this profile view: \n");
            foreach ( ProfileHatchArea oProfileHatchArea in oProfileView.HatchAreas ) {
                ed.WriteMessage(" Hatch area: " + oProfileHatchArea.Name + " shape style: " + oProfileHatchArea.ShapeStyleName + "\n");
                foreach ( ProfileCriteria oProfileCriteria in oProfileHatchArea.Criteria ) {
                    ed.WriteMessage(string.Format("   Criteria: type: {0} profile: {1}\n", oProfileCriteria.BoundaryType.ToString(), oProfileCriteria.ProfileName) );
                }
            }
        }
    }
