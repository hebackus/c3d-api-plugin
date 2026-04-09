<!-- Developer's Guide > API Developer's Guide > Corridors > Baselines >  Adding and Modifying a Baseline Region -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-90887BE8-31DB-4383-B116-F17ABBE5517F.htm -->

#  Adding and Modifying a Baseline Region

Corridor Regions are held in a Baseline's BaselineRegions property, a collection of type BaselineRegionCollection. Regions can be added to and removed from this collection using the Add() and Remove() methods. The Add() method has four versions, all of which take the name of the new region, and either the string name or ObjectId for the document Assembly used to create the region. Two variations take the start and end station for the region. If the stations are not specified, the region is assumed to apply to the whole baseline. Regions cannot overlap, and the Add() method will fail if you try to add a region that overlaps an existing region in the baseline. 

In this example, a baseline is obtained from a specified Corridor, and some information is printed about the region. The region is then removed, and two new regions are added. 
    
    
    // use on a document with at least one alignment, and one profile for the alignment,
    // and a baseline with a BaselineRegion defined.
    // EG: Corridor-5b.dwg in the tutorials directory
    string corridorName = "Corridor - (1)";
    Corridor corridor = ts.GetObject(_civildoc.CorridorCollection[corridorName], OpenMode.ForWrite) as Corridor;
    // get first baseline in corridor
    Baseline baseline = corridor.Baselines[0];
    BaselineRegion baselineRegion = baseline.BaselineRegions[0];
    // print out some properties for this baseline region:
    _editor.WriteMessage("Baseline region name: {0} start station: {1}  end station: {2}", 
        baselineRegion.Name, baselineRegion.StartStation, baselineRegion.EndStation);                    
    
    // Remove the existing baseline region
    baseline.BaselineRegions.Remove(baselineRegion);
    // Add two new baseline regions
    // This will fail if there is already a baselineRegion for the same start-end station range
    ObjectId assemblyId = _civildoc.AssemblyCollection[0];
    baseline.BaselineRegions.Add("New Region1", assemblyId, baseline.StartStation, baseline.EndStation / 2);
    baseline.BaselineRegions.Add("New Region2", assemblyId, baseline.EndStation / 2, baseline.EndStation);
