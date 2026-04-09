<!-- Developer's Guide > API Developer's Guide > Sections Overview > Sections >  Using Sections -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-E6623FD2-97BC-4CF7-96BD-4F433D20BA31.htm -->

#  Using Sections

Each sample line contains a collection of sections that were based on that sample line. Each section is represented by object of type Section and contains methods for retrieving statistics of the surface along the section. 

Note that there is a naming ambiguity between Autodesk.Civil.DatabaseServices.Section and Autodesk.AutoCAD.DatabaseServices.Section. You can resolve this by fully qualifying the class name in your code, or disambiguate the reference with a using alias statement such as: 
    
    
    using Section = Autodesk.Civil.DatabaseServices.Section;

In this example, we get the first SampleLineGroup for an Alignment, iterate the SampleLines in the SampleLineGroup, and then iterate each Section on SampleLine. We print out elevation information for the Section, and set the update mode. 
    
    
    // Use Centerline (1)
    Alignment alignment = null;
    foreach (ObjectId alignmentId in _civildoc.GetAlignmentIds())
    {
        Alignment a = ts.GetObject(alignmentId, OpenMode.ForRead) as Alignment;
        if (a.Name == "Centerline (1)") { alignment = a; break; }
    }
    // Get the first sample line group, SLG-1:
    SampleLineGroup sampleLineGroup = ts.GetObject(alignment.GetSampleLineGroupIds()[0], OpenMode.ForRead) as SampleLineGroup;
    foreach (ObjectId sampleLineId in sampleLineGroup.GetSampleLineIds())
    {
        SampleLine sampleLine = ts.GetObject(sampleLineId, OpenMode.ForRead) as SampleLine;
                        
        foreach ( ObjectId sectionId in sampleLine.GetSectionIds()){
            Section section = ts.GetObject(sectionId, OpenMode.ForWrite) as Section;
            _editor.WriteMessage("Section {0} elevation max: {1} min: {2}\n", section.Name, section.MaximumElevation, section.MinmumElevation);
            // set the section update mode:
            section.UpdateMode = SectionUpdateType.Dynamic;
        }
    }
