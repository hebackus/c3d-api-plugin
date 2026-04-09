<!-- Developer's Guide > API Developer's Guide > Profiles > Profiles > Creating a Profile Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-085E67A0-090B-46E0-8646-BD4B24DB3732.htm -->

# Creating a Profile Style

The profile style, an object of type ProfileStyle, defines the visual display of profiles. The collection of all such styles in a document are stored in the CivilDocument.Styles.ProfileStyles collection. The style contains properties of type DisplayStyle which govern the display of arrows showing alignment direction and of the lines, line extensions, curves, parabolic curve extensions, symmetrical parabolas and asymmetrical parabolas that make up a profile. The properties of a new profile style are defined by the document’s ambient settings.
    
    
    // Illustrates creating a new profile style
    [CommandMethod("CreateProfileStyle")]
    public void CreateProfileStyle()
    {
        doc = CivilApplication.ActiveDocument;
     
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.Database.TransactionManager.StartTransaction())
        {
            ObjectId profileStyleId = doc.Styles.ProfileStyles.Add("New Profile Style");
            ProfileStyle oProfileStyle = ts.GetObject(profileStyleId, OpenMode.ForRead) as ProfileStyle;
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Arrow).Visible = true;
            // set to yellow:
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Line).Color = Color.FromColorIndex(ColorMethod.ByAci, 50);
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Line).Visible = true;
            // grey
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.LineExtension).Color = Color.FromColorIndex(ColorMethod.ByAci, 251);
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.LineExtension).Visible = true;
            // green
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Curve).Color = Color.FromColorIndex(ColorMethod.ByAci, 80);
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.Curve).Visible = true;
            // grey
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.ParabolicCurveExtension).Color = Color.FromColorIndex(ColorMethod.ByAci, 251);
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.ParabolicCurveExtension).Visible = true;
            // green
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.SymmetricalParabola).Color = Color.FromColorIndex(ColorMethod.ByAci, 81);
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.SymmetricalParabola).Visible = true;
            // green
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.AsymmetricalParabola).Color = Color.FromColorIndex(ColorMethod.ByAci, 83);
            oProfileStyle.GetDisplayStyleProfile(ProfileDisplayStyleProfileType.AsymmetricalParabola).Visible = true;
     
            // properties for 3D should also be set
        }
    }
