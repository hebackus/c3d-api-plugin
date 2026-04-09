<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Root Objects and Common Concepts in COM > Label Styles > Sharing Syles Between Drawings -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-BF53E7E2-B622-47E1-BAC7-0196EAFC3036.htm -->

# Sharing Syles Between Drawings

Label styles, like all style objects, can be shared between drawings. To do this, call the style’s exportTo method, targeting the drawing you want to add the style to. In this example, the first style in the MajorStationLabelStyles collection is exported from the active drawing to another open drawing named Drawing1.dwg:
    
    
    Dim oDocument As AeccDocument
    Set oDocument = oCivilApp.ActiveDocument
    Dim dbDestination As AeccDatabase
    Set dbDestination = oCivilApp.Documents("Drawing1.dwg").Database
    Call oDocument.AlignmentLabelStyles.MajorStationLabelStyles(0).ExportTo(dbDestination)
