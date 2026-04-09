<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Baselines > Accessing and Modifying Baseline Stations -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4ACDBEC9-B935-47F2-B2AA-4BDE63C0BDD4.htm -->

# Accessing and Modifying Baseline Stations

Assembly cross sections are placed at regular intervals along a baseline. The list of all stations where assemblies are located along a baseline can be retrieved using the AeccBaseline.GetSortedStations method while all stations along a baseline region can be retrieved using the AeccBaselineRegion.GetSortedStations method. 
    
    
    Dim v As Variant
    v = oBaselineRegion.GetSortedStations()
    Dim i As Integer
    Debug.Print "Assembly stations:"
    For i = 0 To UBound(v)
        Debug.Print v(i)
    Next i
    

New stations can be added to baselines and baseline regions using the AddStation method. Existing stations can be deleted using the DeleteStation method. DeleteStation includes an optional tolerance parameter, letting you specify a station within a range. You can list all of the stations added to a baseline region with the AeccBaselineRegion.GetAdditionalStation method. AeccBaselineRegion.ClearAdditionalStations removes all added stations within a baseline region and leaves only the original stations created at regular intervals.
    
    
    ' Add an assembly to the baseline at station 12+34.5
    oBaseline.AddStation 1234.5, "Station description"
     
    ' Remove the station located within 0.1 units around 5+67.5
    oBaseline.DeleteStation 567.5, 0.1
