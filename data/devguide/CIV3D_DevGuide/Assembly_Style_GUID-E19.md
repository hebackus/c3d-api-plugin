<!-- Developer's Guide > API Developer's Guide > Corridors > Styles > Assembly Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E19CBBFB-91CE-4EA9-95E1-703C06D90DE3.htm -->

# Assembly Style

The collection of all assembly style objects are found in the CivilDocument.Styles.AssemblyStyles property. The assembly style object contains properties for adjusting the marker types for the assembly attachment points, and each of the standard MarkerType properties. While you can create new styles and edit existing styles, you cannot assign a style to an existing assembly using the Autodesk Civil 3D .NET API.
    
    
    using (Transaction ts = Application.DocumentManager.MdiActiveDocument.
        Database.TransactionManager.StartTransaction())
    {
        ObjectId objId = doc.Styles.AssemblyStyles.Add("Style1");
        AssemblyStyle oAssemblyStyle = ts.GetObject(objId, OpenMode.ForWrite) as AssemblyStyle;
        objId = oAssemblyStyle.MarkerStyleAtMainBaselineId;
        MarkerStyle oMarker = ts.GetObject(objId, OpenMode.ForWrite) as MarkerStyle;
        oMarker.CustomMarkerStyle = CustomMarkerType.CustomMarkerX;
        oMarker.MarkerDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 10);
        oMarker.MarkerDisplayStylePlan.Visible = true;
     
        ts.Commit();
    }
