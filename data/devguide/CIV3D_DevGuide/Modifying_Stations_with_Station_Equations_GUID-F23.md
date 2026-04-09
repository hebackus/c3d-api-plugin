<!-- Developer's Guide > API Developer's Guide > Alignments > Stations > Modifying Stations with Station Equations -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-F23CC3E9-C29D-4B98-90A2-604C3D8BDC81.htm -->

# Modifying Stations with Station Equations

A station is a point along an alignment a certain distance from the start of the alignment. By default the station at the start point of an alignment is 0 and increases contiguously through its length. This can be changed by using _station equations_ , which can renumber stations along an alignment. A station equation is an object of type StationEquation which contains a location along the alignment, a new station number basis, and a flag describing whether station values should increase or decrease from that location on. A collection of these station equations is contained in the Alignment::StationEquations property. 

The following code adds a station equation to an alignment, starting at a point 80 units from the beginning of the alignment, and increasing in value:
    
    
    StationEquation myStationEquation = myAlignment.StationEquations.Add(80, 0, StationEquationType.Increasing);
    

Note:

Some functions, such as Alignment::DesignSpeedCollection::GetDesignSpeed(), require a “raw” station value without regard to modifications made by station equations.
