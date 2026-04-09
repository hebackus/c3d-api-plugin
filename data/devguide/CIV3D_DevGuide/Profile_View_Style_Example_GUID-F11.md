<!-- Developer's Guide > API Developer's Guide > Profiles > Profile Views > Setting Profile View Styles > Profile View Style Example -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F11C020E-F067-4EFA-8BC2-E1BEAFB5359F.htm -->

# Profile View Style Example

This example takes an existing profile view style and modifies its top axis and title:
    
    
    [CommandMethod("ModProfileViewStyle")]
    public void ModProfileViewStyle()
    {
        doc = CivilApplication.ActiveDocument;
     
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            // Get the first style in the document's collection of styles
     
            ObjectId profileViewStyleId = doc.Styles.ProfileViewStyles[0];
            ProfileViewStyle oProfileViewStyle = ts.GetObject(profileViewStyleId, OpenMode.ForRead) as ProfileViewStyle;
     
            // Adjust the top axis.  Put station information here, with the title 
            // at the far left.
            oProfileViewStyle.GetDisplayStylePlan(ProfileViewDisplayStyleType.TopAxis).Visible = true;
            oProfileViewStyle.TopAxis.MajorTickStyle.LabelText = "<[Station Value(Um|FD|P1)]> m";
            oProfileViewStyle.TopAxis.MajorTickStyle.Interval = 164.041995;
            oProfileViewStyle.TopAxis.TitleStyle.OffsetX = 0.13;
            oProfileViewStyle.TopAxis.TitleStyle.OffsetY = 0.0;
            oProfileViewStyle.TopAxis.TitleStyle.Text = "Meters";
            oProfileViewStyle.TopAxis.TitleStyle.Location = Autodesk.Civil.DatabaseServices.Styles.AxisTitleLocationType.TopOrLeft;
     
            // Adjust the title to show the alignment name
            oProfileViewStyle.GraphStyle.TitleStyle.Text = "Profile View of:<[Parent Alignment(CP)]>";
     
            ts.Commit();
        }
    }
