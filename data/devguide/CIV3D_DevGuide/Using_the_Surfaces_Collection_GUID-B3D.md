<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Surfaces in COM > Using the Surfaces Collection -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-B3DD41ED-79E7-42A0-92EE-11E0887F561A.htm -->

# Using the Surfaces Collection

All surfaces in a drawing are located in the AeccDocument.Surfaces collection. Each surface in the collection can be accessed through the AeccSurfaces.Item method, which takes either an integer index or the string name of the surface. The AeccSurfaces.Item method returns a generic reference of type AeccSurface, so you need to check the AeccSurface.Type property to actually determine what kind of surface it is.

This sample examines each surface in the drawing and reports what kind of surface it is:
    
    
    Dim oSurface As AeccSurface
    Dim i As Integer
     
    For i = 0 To oAeccDocument.Surfaces.Count - 1
        Set oSurface = oAeccDocument.Surfaces.Item(i)
        Select Case (oSurface.Type)
            Case aecckGridSurface:
                Dim oGridSurface As AeccGridSurface
                Set oGridSurface = oSurface
                Debug.Print oGridSurface.Name & ": Grid"
            Case aecckTinSurface:
                Dim oTinSurface As AeccTinSurface
                Set oTinSurface = oSurface
                Debug.Print oTinSurface.Name & ": TIN"
            Case aecckGridVolumeSurface:
                Dim oGridVolume As AeccGridVolumeSurface
                Set oGridVolume = oSurface
                Debug.Print oGridVolume.Name & ": Grid Volume"
            Case aecckTinVolumeSurface:
                Dim oTinVolume As AeccTinVolumeSurface
                Set oTinVolume = oSurface
                Debug.Print oTinVolume.Name & ": TIN Valume"
        End Select
    Next i
