<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Surface Style > Creating a Style -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-850D4AC4-4007-448B-8B23-FE3971A4423C.htm -->

# Creating a Style

All surface styles are stored in the AeccDocument.SurfaceStyles collection, an object of type AeccSurfaceStyles. To create a new style, call the AeccSurfaceStyles.Add method with the name of your new style. It is initially set according to the document’s ambient settings.
    
    
    Dim oSurfaceStyle As AeccSurfaceStyle
    oSurfaceStyle = oDocument.SurfaceStyles.Add("New Style")
