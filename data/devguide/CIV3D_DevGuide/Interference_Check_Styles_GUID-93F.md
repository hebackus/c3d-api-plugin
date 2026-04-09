<!-- Developer's Guide > API Developer's Guide > Pipe Networks > Interference Checks > Interference Check Styles -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-93F9A55F-78EB-4271-A35A-E2C3262EE0DF.htm -->

# Interference Check Styles

Either a symbol or a model of the actual intersection region can be drawn at each interference location. The display of these intersections is controlled by an InterferenceStyle object. The collection of all interference style objects in the document are stored in the CivilDocument.Styles.InterferenceStyles collection. 

There are three different styles of interference displays you can chose from. First, you can display a 3D model of the intersection region. This is done by setting the ModelOptions style property to InterferenceModelType.TrueSolid. The GetDisplayStyleModel() method returns an object of type DisplayStyle which controls the visible appearance of the model such as color and line types. Make sure the DisplayStyle.Visible property is set to True.

Another possibility is to draw a 3D sphere at the location of the intersection. This is done by setting the ModelOptions style property to InterferenceModelType.Sphere. If the ModelSizeType property is set to InterferenceModelSizeType.SolidExtents, then the sphere is automatically sized to just circumscribe the region of intersection (that is, it is the smallest sphere that still fits the model of the intersection region). You can set the size of the sphere by setting the ModelSizeType property to InterferenceModelSizeType.UserSpecified, setting the ModelSizeOptions property to use either absolute units or drawing units, and setting the corresponding AbsoluteModelSize or DrawingScaleModelSize property to the desired value. Again, the DisplayStyle object returned by GetDisplayStyleModel() controls the visual features such as color and line type.

The third option is to place a symbol at the location of intersection. Set the GetDisplayStylePlan(InterferenceDisplayStyleType.Symbol).Visible property to True to make symbols visible. The style property MarkerStyle, an object of type MarkerStyle, controls all aspects of how the symbol is drawn.

This sample creates a new interference style object that displays an X symbol with a superimposed circle at points of intersection:
    
    
    public void InterfStyle()
    {
        CivilDocument doc = CivilApplication.ActiveDocument;
        Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
        using (Transaction ts = Application.DocumentManager.MdiActiveDocument.
           Database.TransactionManager.StartTransaction())
        {
            ObjectId intStyleId;
            intStyleId = doc.Styles.InterferenceStyles.Add("Interference style 01");
            InterferenceStyle oIntStyle = ts.GetObject(intStyleId, OpenMode.ForWrite) as InterferenceStyle;
            // Draw a symbol of a violet X with circle with a specified
            // drawing size at the points of intersection.
            oIntStyle.GetDisplayStylePlan(InterferenceDisplayStyleType.Symbol).Visible = true;
            ObjectId markerStyleId = oIntStyle.MarkerStyle;
            MarkerStyle oMarkerStyle = ts.GetObject(markerStyleId, OpenMode.ForWrite) as MarkerStyle;
            oMarkerStyle.MarkerType = MarkerDisplayType.UseCustomMarker;
            oMarkerStyle.CustomMarkerStyle = CustomMarkerType.CustomMarkerX;
            oMarkerStyle.CustomMarkerSuperimposeStyle = CustomMarkerSuperimposeType.Circle;
            oMarkerStyle.MarkerDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 200);
            oMarkerStyle.MarkerDisplayStylePlan.Visible = true;
            oMarkerStyle.SizeType = MarkerSizeType.AbsoluteUnits;
            oMarkerStyle.MarkerSize = 5.5;
            // Hide any model display at intersection points.
            oIntStyle.GetDisplayStyleModel(InterferenceDisplayStyleType.Solid).Visible = false;
            ts.Commit();
        }
        
    }
