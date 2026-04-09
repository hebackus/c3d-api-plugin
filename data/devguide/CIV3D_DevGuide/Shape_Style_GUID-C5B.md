<!-- Developer's Guide > API Developer's Guide > Corridors > Styles > Shape Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-C5B574DA-B8DF-444E-94AF-F2E25DA3B1DF.htm -->

# Shape Style

The collection of all shape style objects are found in the CivilDocument.ShapeStyles property. This style object contains properties for adjusting the visual display of assembly and subassembly shapes, including the outline and the inside area. 

Note:

Shape style objects are not used directly with shape objects, but are instead used with roadway style sets.
    
    
    // Create a new shape style and change it so that it has
    // an orange border and a yellow hatch fill.
    objId = doc.Styles.ShapeStyles.Add("Style3");
    ShapeStyle oShapeStyle = ts.GetObject(objId, OpenMode.ForWrite) as ShapeStyle;
    // 50 = yellow
    oShapeStyle.AreaFillDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 50);
    oShapeStyle.AreaFillDisplayStylePlan.Visible = true;
    oShapeStyle.AreaFillHatchDisplayStylePlan.HatchType = HatchType.PreDefined;
    oShapeStyle.AreaFillHatchDisplayStylePlan.Pattern = "LINE";
    // 30 = orange
    oShapeStyle.BorderDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 30);
    oShapeStyle.BorderDisplayStylePlan.Visible = true;
     
    ts.Commit();
