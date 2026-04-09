<!-- Developer's Guide > API Developer's Guide > Corridors > Baselines > Listing Baseline Regions -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-A302BCDD-D4C8-43EF-B481-1EBB6CE9EED0.htm -->

# Listing Baseline Regions

The collection of all the regions of a baseline are contained in the Baseline.BaselineRegions property.

The Autodesk Civil 3D API does not include methods for creating new baseline regions, or manipulating existing regions.

The following sample displays the start and end station for every baseline region in a baseline:
    
    
    foreach (BaselineRegion oBaselineRegion in oBaseline.BaselineRegions)
    {
        ed.WriteMessage(@"Baseline region information - 
      Start station : {0}
      End station   : {1}\n",                          
      oBaselineRegion.StartStation,
      oBaselineRegion.EndStation);
     
    }
