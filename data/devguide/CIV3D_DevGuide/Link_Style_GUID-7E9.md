<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Styles > Link Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-7E99DAF9-3E8E-4025-B886-86750916767C.htm -->

# Link Style

The collection of all link style objects are found in the AeccRoadwayDocument.LinkStyles property. This style object contains properties for adjusting the visual display of assembly and subassembly links.

Note:

Link style objects are not used directly with link objects, but are instead used with roadway style sets.
    
    
    ' Create a new link style and color it green.
    Dim oLinkStyle As AeccRoadwayLinkStyle
    Set oLinkStyle = oRoadwayDocument.LinkStyles.Add("Style2")
    With oLinkStyle
        .LinkDisplayStylePlan.color = 80
        .LinkDisplayStylePlan.Visible = True
    End With
