<!-- Developer's Guide > API Developer's Guide > Corridors > Baselines > Adding a Baseline to a Corridor -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-8667E32E-CDD8-4FC9-8246-4789725DA337.htm -->

# Adding a Baseline to a Corridor

The BaselineCollection class allows you to add a new Baseline to a Corridor using the Add() method. There are two versions of this method. One takes the name of the new Baseline, the ObjectId of the Alignment, and the ObjectId of a Profile. The second takes the name of the new Baseline, the name of the Alignment, and the name of a Profile.

In this example, a corridor is selected by name, and the first alignment in the document and the first profile in the alignment are used to create a baseline. 
    
    
    // use on a document with at least one alignment, and one profile for the alignment
    // EG: Corridor-5b.dwg in the tutorials directory
    string corridorName = "Corridor - (1)";
    Corridor corridor = ts.GetObject(_civildoc.CorridorCollection[corridorName], OpenMode.ForWrite) as Corridor;
    
    // Get the ObjectId of an alignment and profile
    ObjectId alignmentId = _civildoc.GetAlignmentIds()[0];
    Alignment alignment = ts.GetObject(alignmentId, OpenMode.ForRead) as Alignment;
    ObjectId profileId = alignment.GetProfileIds()[0];
    
    Baseline baseline = corridor.Baselines.Add("New Baseline", alignmentId, profileId);
