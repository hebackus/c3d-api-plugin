<!-- Developer's Guide > API Developer's Guide > Sections Overview > Sections > Creating Sections -->
<!-- Source: https://help.autodesk.com/cloudhelp/2026/ENU/Civil3D-DevGuide/files/GUID-611DE133-40A0-4F0F-8622-1489561AEC27.htm -->

# Creating Sections

Sections are created on a SampleLineGroup by getting the collection of possible SectionSources returned by GetSectionSources(). This is a collection of ObjectIds for SectionSource objects. By default, this collection contains a SectionSource for every possible Surface and Corridor Shape available. The type of object the SectionSource is related to is held in its SourceType property. To sample a specific Surface or Corridor Shape, its corresponding SectionSource.IsSampled property is set to True.

In this example, a user is prompted to select an Alignment. A new SampleLineGroup is created, and then the SampleLineGroup's SectionSourceCollection is iterated. The SectionSource for the TIN Surface is sampled. 
    
    
    // prompt user to select an alignment, and then create a new SampleLineGroup for the Alignment:
    ObjectId alignmentId = promptForEntity("Select an Alignment to add sample lines to:", typeof(Alignment));
    Alignment alignment = ts.GetObject(alignmentId, OpenMode.ForWrite) as Alignment;
    ObjectId sampleLineGroupId = SampleLineGroup.Create("New Group", alignmentId);
    SampleLineGroup sampleLineGroup = ts.GetObject(sampleLineGroupId, OpenMode.ForWrite) as SampleLineGroup;
    
    // Create a sample line.
    ObjectId sampleLineId = SampleLine.Create("sample line 1", sampleLineGroupId, alignment.StartingStation);
    
    
    // Get the available section sources for the SampleLineGroup
    // SampleLineGroup must be OpenMode.ForWrite for this to work:
    SectionSourceCollection sectionSources = sampleLineGroup.GetSectionSources();
    _editor.WriteMessage("Number of section sources: {0}\n", sectionSources.Count);
    
    ObjectId surfaceId = ObjectId.Null;
    foreach (SectionSource sectionSource in sectionSources)
    {
        _editor.WriteMessage("Section source is sampled: {0} update mode: {1} type: {2}\n", sectionSource.IsSampled, sectionSource.UpdateMode, sectionSource.SourceType);
        // if it's a TinSurface, let's sample it:
        if (sectionSource.SourceType == SectionSourceType.TinSurface)
        {
            // save for later:
            surfaceId = sectionSource.SourceId;
            // we can also get more info about the source type from its objectId
            TinSurface sourceSurface = ts.GetObject(sectionSource.SourceId, OpenMode.ForRead) as TinSurface;
            _editor.WriteMessage("Adding TIN surface {0} to Section Sources for SampleLineGroup\n", sourceSurface.Name);
            sectionSource.IsSampled = true;
        }
    }
    

Surfaces and Corridor Shapes are also used to make volume calculations for Quantity Takeoff tables. These Surfaces and shapes are represented by MaterialSectionSource objects. Unlike SectionSource objects, the isSampled property is read-only, and is not used to sample the source. To sample a Surface or Shape, it is added to a QTOMaterial by the QTOMaterial.Add() method. 

There are multiple steps to adding a Surface or Shape to a QTOMaterial. First a QTOMaterialList is added to a SampleLineGroup with the SampleLineGroup.MaterialLists.Add() method. Then A new QTOMaterial is added to the QTOMaterialList. Finally, the Surface or Shape is added to the QTOMaterial.

The code snippet below illustrates these steps. It continues from the sample provided above (using the stored surfaceId used as a SectionSource). 
    
    
    // Material Sources are grouped in QTOMaterialLists, so we create a QTOMaterialList first:
    QTOMaterialList qtoMaterialList = sampleLineGroup.MaterialLists.Add("New Material List");
    // Add the material:
    QTOMaterial qtoMaterial = qtoMaterialList.Add("New Material");
    // Add the material item to either a surface or a corridor shape code.  
    // Here we use the TIN surface ID for EG sampled above:             
    qtoMaterial.Add(surfaceId);
    
    // This is how you access all the Material Section Sources:
    // Get the material sources
    MaterialSectionSourceCollection materialSectionSources = sampleLineGroup.GetMaterialSectionSources();
    _editor.WriteMessage("Number of material section sources: {0}\n", materialSectionSources.Count);
    
    // Note that unlike SectionSource, isSampled is read-only
    foreach (MaterialSectionSource materialSectionSource in materialSectionSources)
    {
        _editor.WriteMessage("Material source is sampled: {0} update mode: {1} type: {2} material: {3}\n", materialSectionSource.IsSampled,
            materialSectionSource.UpdateMode, materialSectionSource.SourceType, materialSectionSource.Material);
    }
