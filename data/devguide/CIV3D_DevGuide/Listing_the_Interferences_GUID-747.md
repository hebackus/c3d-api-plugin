<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Pipe Networks in COM > Interference Checks > Listing the Interferences -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-7471EE8E-A0AD-4E73-8B8E-BFCF822B7442.htm -->

# Listing the Interferences

An interference check, the AeccInterferenceCheck object returned by the AeccInterferenceChecks.Create method, contains a collection of AeccInterference objects each representing a single interference found during the check. Each interference holds the point location of the interference center in the Location property, a three element array of doubles representing X, Y, and Z coordinates. The bounds of the entire interference area are returned by the GetExtents method. The extents are a two-item array of points, together representing the greatest and least corners of a cube containing the intersection area. The SourceNetworkPart and TargetNetworkPart properties hold the network parts that intersect.
    
    
    Dim oInterference As AeccInterference
    For Each oInterference In oInterferenceCheck
        ' Display the 2D x,y location of the interference.
        Dim vLocation As Variant
        Dim sLocation As String
        Dim vExtent As Variant
        vLocation = oInterference.Location
        sLocation = vLocation(0) & ", " & vLocation(1)
        MsgBox "There is an interference at:" & sLocation
     
        ' Display the greatest and least corners of the 3D
        ' rectangle containing the interference.
        vExtent = oInterference.GetExtents()
        Debug.Print "The interference takes place between:"
        sLocation = vExtent(0)(0) & ", "
        sLocation = sLocation & vExtent(0)(1) & ", "
        sLocation = sLocation & vExtent(0)(2)
        Debug.Print "  "; sLocation; "   and:"
        sLocation = vExtent(1)(0) & ", "
        sLocation = sLocation & vExtent(1)(1) & ", "
        sLocation = sLocation & vExtent(1)(2)
        Debug.Print "  "; sLocation
    Next
     
    If (oInterferenceCheck.Count = 0) Then
        MsgBox "There are no interferences in the network."
    End If
