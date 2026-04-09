<!-- Developer's Guide > API Developer's Guide > Alignments > Stations > Creating Station Sets -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-95951E79-61BF-4FF2-9E89-9D96957AEAD2.htm -->

# Creating Station Sets

Alignment stations are usually labeled at regular intervals. You can compute the number, location, and geometry of stations taken at regular spacings by using the Alignment::GetStationSet() method. Overloads of this method return a collection of stations based on the type of station requested, and optionally major and minor intervals. 
    
    
    // Get all the potential stations with major interval = 100, and minor interval = 20
    // Print out the raw station number, type, and location
    Station[] myStations = myAlignment.GetStationSet( StationType.All,100,20);
    ed.WriteMessage("Number of possible stations: {0}\n", myStations.Length);
    foreach (Station myStation in myStations){                    
            ed.WriteMessage("Station {0} is type {1} and at {2}\n", myStation.RawStation, myStation.StnType.ToString(), myStation.Location.ToString());                    
    }
