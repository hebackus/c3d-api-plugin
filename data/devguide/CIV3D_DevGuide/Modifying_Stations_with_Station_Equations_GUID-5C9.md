<!-- Developer's Guide > API Developer's Guide > Legacy COM API > Alignments in COM > Stations > Modifying Stations with Station Equations -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-5C965285-8A83-4BBE-B77B-EC27EFE395BE.htm -->

# Modifying Stations with Station Equations

A station is a point along an alignment a certain distance from the start of the alignment. By default the station at the start point of an alignment is 0 and increases contiguously through its length. This can be changed by using _station equations_ , which can renumber stations along an alignment. A station equation is an object of type AeccStationEquation which contains a location along the alignment, a new station number basis, and a flag describing whether station values should increase or decrease from that location on. A collection of these station equations is contained in the AeccAlignment.StationEquations property. 

The following code changes an alignment so that at a point 80 units from the beginning, stations will start being numbered from the value 720:
    
    
    Dim oStationEquation As AeccStationEquation
    Set oStationEquation = oAlignment.StationEquations _
      .Add(80, 0, 720, aeccIncreasing)
    

Note:

Some functions, such as AeccAlignment.InstantaneousRadius, require a “raw” station value without regard to modifications made by station equations.
