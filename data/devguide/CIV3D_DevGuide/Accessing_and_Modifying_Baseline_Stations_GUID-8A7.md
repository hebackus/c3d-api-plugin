<!-- Developer's Guide > API Developer's Guide > Corridors > Baselines > Accessing and Modifying Baseline Stations -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8A7BD03B-129B-4C7A-93E1-ADA244E1BFB1.htm -->

# Accessing and Modifying Baseline Stations

Assembly cross sections are placed at regular intervals along a baseline. The list of all stations where assemblies are located along a baseline can be retrieved using the Baseline.SortedStations() method, while all stations along a baseline region can be retrieved using the BaselineRegion.SortedStations() method. 
    
    
    double[] stations = oBaselineRegion.SortedStations();
    ed.WriteMessage("Baseline Region stations: \n");
    foreach (double station in stations){
        ed.WriteMessage("\tStation: {0}\n", station);
    }
    

New stations can be added to baseline regions using the AddStation() method. Existing stations can be deleted using the DeleteStation method. DeleteStation includes an optional tolerance parameter, letting you specify a station within a range. You can list all of the stations added to a baseline region with the BaselineRegion.GetAdditionalStation method. BaselineRegion.ClearAdditionalStations removes all added stations within a baseline region and leaves only the original stations created at regular intervals.
    
    
    // Add an assembly to the middle of the baseline region
    double newStation = oBaselineRegion.StartStation + 
        ((oBaselineRegion.EndStation - oBaselineRegion.StartStation) / 2);
    oBaselineRegion.AddStation(newStation, "New Station");
    ed.WriteMessage("Added New Station: {0}", newStation);
     
    // Remove the station located at the beginning of the baseline region:
    oBaselineRegion.DeleteStation(oBaselineRegion.StartStation);
