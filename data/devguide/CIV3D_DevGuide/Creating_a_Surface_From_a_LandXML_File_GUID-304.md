<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Creating a Surface > Creating a Surface From a LandXML File -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-304CD53C-0B7B-415D-8746-F7318743C5D7.htm -->

# Creating a Surface From a LandXML File

A surface saved as a LandXML file can be loaded using the AeccSurfaces.ImportXML method. The file also describes the kind of surface to be created, so you do not need to know beforehand. After the surface has been loaded, you can examine the AeccSurface.Type property and assign the generic surface reference to a more specific type.
    
    
    Dim oSurface As AeccSurface
    Dim sFileName As String
    sFileName = "C:\My Documents\EG.xml"
    Set oSurface = oAeccDocument.Surfaces.ImportXML(sFileName)
     
    Dim oTinSurface as AeccTinSurface
    If (oSurface.Type = aecckTinSurface) Then
        Set oTinSurface = oSurface
    End If
