<!-- Developer's Guide > API Developer's Guide > Corridors > Baselines > Listing Baselines in a Corridor -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-9CD5C53D-3DA6-454F-8A0B-190E10B9E283.htm -->

# Listing Baselines in a Corridor

The collection of all baselines in a corridor are contained in the Corridor.Baselines property, which is type BaselineCollection.

The following sample displays information about the underlying alignment and profile for every baseline in a corridor:
    
    
    foreach (Baseline oBaseline in oCorridor.Baselines)
    {                       
        Alignment oAlign = ts.GetObject(oBaseline.AlignmentId, OpenMode.ForRead) as Alignment;
        Profile oProfile = ts.GetObject(oBaseline.ProfileId, OpenMode.ForRead) as Profile;
        ed.WriteMessage(@"Baseline information - 
          Alignment     : {0}
          Profile       : {1}
          Start station : {2}
          End station   : {3}", 
          oAlign.Name,
          oProfile.Name,
          oBaseline.StartStation,
          oBaseline.EndStation);
    }
