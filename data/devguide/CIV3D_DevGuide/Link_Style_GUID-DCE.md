<!-- Developer's Guide > API Developer's Guide > Corridors > Styles > Link Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-DCE208B6-6B5E-4901-B318-3FE7364CE3AB.htm -->

# Link Style

The collection of all link style objects are found in the CivilDocument.Styles.LinkStyles property. This style object contains properties for adjusting the visual display of assembly and subassembly links.

Note:

Link style objects are not used directly with link objects, but are instead used with roadway style sets.
    
    
    // Add a new link style to the document:
    objId = doc.Styles.LinkStyles.Add("Style2");
    LinkStyle oLinkStyle = ts.GetObject(objId, OpenMode.ForWrite) as LinkStyle;
    oLinkStyle.LinkDisplayStylePlan.Color = Color.FromColorIndex(ColorMethod.ByAci, 80);
    oLinkStyle.LinkDisplayStylePlan.Visible = true;
     
    ts.Commit();
