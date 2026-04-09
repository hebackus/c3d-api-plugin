<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Baselines > Listing Baselines in a Corridor -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-7FB74536-C9CE-420B-BF54-7C0D57C7838E.htm -->

# Listing Baselines in a Corridor

The collection of all baselines in a corridor are contained in the AeccCorridor.Baselines property.

The following sample display information about the underlying alignment and profile for every baseline in a corridor:
    
    
    Dim oBaseline As AeccBaseline
    For Each oBaseline In oCorridor.Baselines
        Debug.Print "Baseline information -"
        Debug.Print "Alignment    : " & oBaseline.Alignment.Name
        Debug.Print "Profile      : " & oBaseline.Profile.Name
        Debug.Print "Start station: " & oBaseline.StartStation
        Debug.Print "End station  : " & oBaseline.EndStation
        Debug.Print
    Next
