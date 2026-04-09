<!-- Developer's Guide > API Developer's Guide > Sections Overview > Sample Lines -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-6A1012A4-1B8B-4109-9515-EBBE8121842F.htm -->

# Sample Lines

SampleLine objects are held in an Alignment's SampleLineGroup collection, which is obtained with the Alignment.GetSampleLineGroupIds() method. The collection of SampleLine objects in a SampleLineGroup is obtained with the SampleLineGroup.GetSamleLineIds() method. This example illustrates how to access both these collections, by listing all the SampleLineGroups and SampleLines for the first Alignment in a drawing: 
    
    
    ObjectId alignmentId = _civildoc.GetAlignmentIds()[0];
    Alignment alignment = ts.GetObject(alignmentId, OpenMode.ForRead) as Alignment;
    
    foreach (ObjectId oid in alignment.GetSampleLineGroupIds())
    {
        SampleLineGroup sampleLineGroup = ts.GetObject(oid, OpenMode.ForRead) as SampleLineGroup;
        _editor.WriteMessage("Sample Line Group: {0}\n", sampleLineGroup.Name);
        foreach (ObjectId sampleLineId in sampleLineGroup.GetSampleLineIds())
        {
            SampleLine sampleline = ts.GetObject(sampleLineId, OpenMode.ForRead) as SampleLine;
            _editor.WriteMessage("Sample Line: {0}\n", sampleline.Name);
        }
    
    }
    

You can create new SampleLines using the SampleLine.Create() static method, which takes the name of the new SampleLine, the ObjectId of the SampleLineGroup to add the SampleLine to, and either a station number (the RawStation number, as Double) or a Point2dCollection containing points defining the vertex of the new SampleLine.

In this example, the user is prompted to select an Alignment, and SampleLines are added for each major station on the Alignment. 
    
    
    // prompt user for Alignment
    ObjectId alignmentId = promptForEntity("Select an Alignment to add sample lines to:", typeof(Alignment));
    Alignment alignment = ts.GetObject(alignmentId, OpenMode.ForWrite) as Alignment;
    ObjectId sampleLineGroupId = SampleLineGroup.Create("New Group", alignmentId);
    SampleLineGroup sampleLineGroup = ts.GetObject(sampleLineGroupId, OpenMode.ForWrite) as SampleLineGroup;
    
    Station[] majorStations = alignment.GetStationSet(StationTypes.Major);
    
    foreach (Station station in majorStations)
    {
        ObjectId sampleLineId = SampleLine.Create("SampleLine" + station.RawStation, sampleLineGroupId, station.RawStation);
        SampleLine sampleLine = ts.GetObject(sampleLineId, OpenMode.ForWrite) as SampleLine;
        sampleLine.StyleName = "Standard";
    }
