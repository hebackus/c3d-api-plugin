<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Corridors in COM > Baselines > Listing Offset Baselines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-4D604DBA-7BEA-4D44-9DC5-BA7EB323A5E8.htm -->

# Listing Offset Baselines

Within a baseline region, it is possible to have secondary baselines that are offset from the main baseline. The collection of these offset baselines are contained in the AeccBaselineRegion.OffsetBaselines property. The collection contains two kinds of baselines derived from the IAeccBaseBaseline interface. One is the hardcoded offset baseline (an instances of the AeccHardcodedOffsetBaseline class) which is a constant distance from the main baseline for the entire length of the offset baseline. The other is offset baseline (an instance of the AeccOffsetBaseline class), which is a variable distance from the main baseline.

Note:

The Autodesk Civil 3D API does not include methods for creating new offset baselines or hardcoded offset baselines.

This code examines each offset baseline within a baseline region:
    
    
    Dim oBaseBaseline As IAeccBaseBaseline
    For Each oBaseBaseline In oBaselineRegion.OffsetBaselines
       Dim dMainStart As Double ' station on main baseline
       Dim dMainEnd As Double ' station on main baseline
       Dim vOE As Variant
     
       Select Case oBaseline.Type
       Case aeccCorridorOffsetBaseline
          Dim oOffsetBaseline As AeccOffsetBaseline
          Set oOffsetBaseline = oBaseBaseline
     
          ' Report that an offset baseline exists.
          dMainStart = oOffsetBaseline.StartStationOnMainBaseline
          dMainEnd = oOffsetBaseline.EndStationOnMainBaseline
          Debug.Print "Offset baseline, station " & dMainStart & _
             " to " & dMainEnd
     
          ' Report the offset of the baseline at its start and end.
          vOE = oOffsetBaseline. _
             GetOffsetElevationFromMainBaselineStation(dMainStart)
          Debug.Print " is offset by: " & _ 
             vOE(0) & " horizontal and: " & vOE(1) & _
             " vertical at start"
          vOE = oOffsetBaseline. _
             GetOffsetElevationFromMainBaselineStation(dMainEnd)
          Debug.Print " is offset by: " & vOE(0) & _
             " horizontal and: " & vOE(1) & " vertical at end"
     
       Case aeccCorridorHardcodedOffsetBaseline
          Dim oHardcodedOffsetBaseline As AeccHardcodedOffsetBaseline
          Set oHardcodedOffsetBaseline = oBaseBaseline
     
          ' Report that a hardcoded offset baseline exists.
          dMainStart = oHardcodedOffsetBaseline.StartStation
          dMainEnd = oHardcodedOffsetBaseline.EndStation
          Debug.Print "Hardcoded offset baseline, station " _
             & dMainStart & " to " & dMainEnd
          vOE = oHardcodedOffsetBaseline. _
             OffsetElevationFromMainBaseline
          Debug.Print " is offset by: " & vOE(0) & _
             " horizontal and: " & vOE(1) & " vertical"
       End Select
    Next
