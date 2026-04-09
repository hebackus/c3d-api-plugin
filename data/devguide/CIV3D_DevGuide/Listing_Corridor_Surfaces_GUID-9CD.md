<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Corridor Surfaces > Listing Corridor Surfaces -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9CD18ABC-69F4-4979-94B3-E679A4656A26.htm -->

# Listing Corridor Surfaces

The collection of all corridor surfaces for each corridor is held in the the AeccCorridor.CorridorSurfaces property. Each corridor surface contains the boundary of the surface and a list of all point, link, and feature line codes used in the construction of the surface. Corridor surfaces also contain read-only references to the surface style and section style used in drawing the surface.

Note:

The Autodesk Civil 3D API does not include methods for creating new corridor surfaces or modifying existing corridor surfaces.

This sample lists all the corridor surfaces within a corridor and specifies which point codes were used:
    
    
    Dim oCorridorSurface As AeccCorridorSurface
    For Each oCorridorSurface In oCorridor.CorridorSurfaces
        Debug.Print "Surface name: "; oCorridorSurface.Name
     
        ' Get the point codes that were used to construct
        ' this surface.
        Dim sCodes() As String
        Dim sCodeList As String
        Dim i as Integer
        sCodes = oCorridorSurface.PointCodes
        For i = 0 To UBound(sCodes)
            sCodeList = sCodeList & " " & sCodes(i)
        Next i
        Debug.Print "Point codes: " & sCodeList
    Next
