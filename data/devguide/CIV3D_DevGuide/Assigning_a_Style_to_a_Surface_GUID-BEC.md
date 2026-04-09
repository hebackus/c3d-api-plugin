<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Surface Style > Assigning a Style to a Surface -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-BEC832E5-2BCA-452D-AA89-EADD93094371.htm -->

# Assigning a Style to a Surface

Set the AeccSurface.Style property to the name of the style you wish to use.
    
    
    ' The surface is displayed according to the 
    ' oSurfaceStyle style we have just created.
    oSurface.Style = oSurfaceStyle.Name
